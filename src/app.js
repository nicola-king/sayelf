import {
  addMessage,
  createConversation,
  createEmptyState,
  deleteConversation,
  exportConversation,
  loadState,
  renameConversation,
  saveState,
  setActiveConversation,
} from './conversationStore.js';

const elements = {
  conversationList: document.querySelector('[data-conversation-list]'),
  emptyState: document.querySelector('[data-empty-state]'),
  messageList: document.querySelector('[data-message-list]'),
  messageForm: document.querySelector('[data-message-form]'),
  messageInput: document.querySelector('[data-message-input]'),
  roleSelect: document.querySelector('[data-role-select]'),
  newConversationButton: document.querySelector('[data-new-conversation]'),
  renameButton: document.querySelector('[data-rename-conversation]'),
  deleteButton: document.querySelector('[data-delete-conversation]'),
  exportButton: document.querySelector('[data-export-conversation]'),
  title: document.querySelector('[data-active-title]'),
  meta: document.querySelector('[data-active-meta]'),
};

let state = loadState();

if (state.conversations.length === 0) {
  state = createConversation(createEmptyState(), 'Welcome');
  state = addMessage(
    state,
    state.activeConversationId,
    'assistant',
    'Start a conversation by adding notes, user messages, or assistant replies. Everything is saved in this browser.',
  );
  persist();
}

function persist() {
  saveState(state);
}

function getActiveConversation() {
  return state.conversations.find(
    (conversation) => conversation.id === state.activeConversationId,
  );
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

function renderConversationList() {
  elements.conversationList.replaceChildren(
    ...state.conversations.map((conversation) => {
      const button = document.createElement('button');
      button.className = 'conversation-card';
      button.type = 'button';
      button.dataset.active = String(conversation.id === state.activeConversationId);
      button.addEventListener('click', () => {
        state = setActiveConversation(state, conversation.id);
        persist();
        render();
      });

      const title = document.createElement('strong');
      title.textContent = conversation.title;

      const meta = document.createElement('span');
      const messageCount = conversation.messages.length;
      meta.textContent = `${messageCount} message${messageCount === 1 ? '' : 's'} · ${formatDate(
        conversation.updatedAt,
      )}`;

      button.append(title, meta);
      return button;
    }),
  );
}

function renderMessages(conversation) {
  elements.emptyState.hidden = Boolean(conversation);
  elements.messageForm.hidden = !conversation;
  elements.renameButton.disabled = !conversation;
  elements.deleteButton.disabled = !conversation;
  elements.exportButton.disabled = !conversation;

  if (!conversation) {
    elements.title.textContent = 'No conversation selected';
    elements.meta.textContent = 'Create a conversation to get started.';
    elements.messageList.replaceChildren();
    return;
  }

  elements.title.textContent = conversation.title;
  elements.meta.textContent = `Updated ${formatDate(conversation.updatedAt)}`;
  elements.messageList.replaceChildren(
    ...conversation.messages.map((message) => {
      const article = document.createElement('article');
      article.className = `message message--${message.role}`;

      const header = document.createElement('header');
      header.textContent = `${message.role} · ${formatDate(message.createdAt)}`;

      const body = document.createElement('p');
      body.textContent = message.content;

      article.append(header, body);
      return article;
    }),
  );
  elements.messageList.scrollTop = elements.messageList.scrollHeight;
}

function render() {
  renderConversationList();
  renderMessages(getActiveConversation());
}

elements.newConversationButton.addEventListener('click', () => {
  const title = window.prompt('Conversation title', 'New conversation');
  if (title === null) return;

  state = createConversation(state, title);
  persist();
  render();
  elements.messageInput.focus();
});

elements.renameButton.addEventListener('click', () => {
  const conversation = getActiveConversation();
  if (!conversation) return;

  const title = window.prompt('Rename conversation', conversation.title);
  if (title === null) return;

  state = renameConversation(state, conversation.id, title);
  persist();
  render();
});

elements.deleteButton.addEventListener('click', () => {
  const conversation = getActiveConversation();
  if (!conversation) return;

  const confirmed = window.confirm(`Delete “${conversation.title}”? This cannot be undone.`);
  if (!confirmed) return;

  state = deleteConversation(state, conversation.id);
  persist();
  render();
});

elements.exportButton.addEventListener('click', async () => {
  const conversation = getActiveConversation();
  if (!conversation) return;

  const text = exportConversation(conversation);
  await navigator.clipboard.writeText(text);
  elements.exportButton.textContent = 'Copied!';
  setTimeout(() => {
    elements.exportButton.textContent = 'Copy markdown';
  }, 1200);
});

elements.messageForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const conversation = getActiveConversation();
  if (!conversation) return;

  state = addMessage(
    state,
    conversation.id,
    elements.roleSelect.value,
    elements.messageInput.value,
  );
  elements.messageInput.value = '';
  persist();
  render();
});

render();
