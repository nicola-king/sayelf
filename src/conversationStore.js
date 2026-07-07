const STORAGE_KEY = 'sayelf.conversations.v1';
const DEFAULT_TITLE = 'New conversation';

const createId = () => {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID();
  }

  return `id-${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

const now = () => new Date().toISOString();

const sortByRecent = (conversations) =>
  [...conversations].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));

const normalizeConversation = (conversation) => ({
  id: conversation.id || createId(),
  title: conversation.title || DEFAULT_TITLE,
  createdAt: conversation.createdAt || now(),
  updatedAt: conversation.updatedAt || conversation.createdAt || now(),
  messages: Array.isArray(conversation.messages) ? conversation.messages : [],
});

export const createEmptyState = () => ({
  activeConversationId: null,
  conversations: [],
});

export const createConversation = (state, title = DEFAULT_TITLE) => {
  const timestamp = now();
  const conversation = {
    id: createId(),
    title: title.trim() || DEFAULT_TITLE,
    createdAt: timestamp,
    updatedAt: timestamp,
    messages: [],
  };

  return {
    activeConversationId: conversation.id,
    conversations: [conversation, ...state.conversations],
  };
};

export const renameConversation = (state, conversationId, title) => {
  const nextTitle = title.trim();
  if (!nextTitle) return state;

  return {
    ...state,
    conversations: state.conversations.map((conversation) =>
      conversation.id === conversationId
        ? { ...conversation, title: nextTitle, updatedAt: now() }
        : conversation,
    ),
  };
};

export const deleteConversation = (state, conversationId) => {
  const conversations = state.conversations.filter(
    (conversation) => conversation.id !== conversationId,
  );
  const activeConversationId =
    state.activeConversationId === conversationId
      ? conversations[0]?.id ?? null
      : state.activeConversationId;

  return { activeConversationId, conversations };
};

export const setActiveConversation = (state, conversationId) => ({
  ...state,
  activeConversationId: state.conversations.some(
    (conversation) => conversation.id === conversationId,
  )
    ? conversationId
    : state.activeConversationId,
});

export const addMessage = (state, conversationId, role, content) => {
  const trimmedContent = content.trim();
  if (!trimmedContent) return state;

  const timestamp = now();
  const message = {
    id: createId(),
    role,
    content: trimmedContent,
    createdAt: timestamp,
  };

  return {
    activeConversationId: conversationId,
    conversations: sortByRecent(
      state.conversations.map((conversation) =>
        conversation.id === conversationId
          ? {
              ...conversation,
              messages: [...conversation.messages, message],
              updatedAt: timestamp,
            }
          : conversation,
      ),
    ),
  };
};

export const loadState = (storage = globalThis.localStorage) => {
  if (!storage) return createEmptyState();

  try {
    const parsed = JSON.parse(storage.getItem(STORAGE_KEY));
    const conversations = sortByRecent(
      Array.isArray(parsed?.conversations)
        ? parsed.conversations.map(normalizeConversation)
        : [],
    );
    const activeConversationId = conversations.some(
      (conversation) => conversation.id === parsed?.activeConversationId,
    )
      ? parsed.activeConversationId
      : conversations[0]?.id ?? null;

    return { activeConversationId, conversations };
  } catch {
    return createEmptyState();
  }
};

export const saveState = (state, storage = globalThis.localStorage) => {
  if (!storage) return;
  storage.setItem(STORAGE_KEY, JSON.stringify(state));
};

export const exportConversation = (conversation) => {
  const lines = [`# ${conversation.title}`, ''];
  for (const message of conversation.messages) {
    lines.push(`**${message.role}** (${new Date(message.createdAt).toLocaleString()}):`);
    lines.push(message.content);
    lines.push('');
  }
  return lines.join('\n');
};
