import assert from 'node:assert/strict';
import test from 'node:test';

import {
  addMessage,
  createConversation,
  createEmptyState,
  deleteConversation,
  exportConversation,
  loadState,
  renameConversation,
  saveState,
} from '../src/conversationStore.js';

const createMemoryStorage = () => {
  const values = new Map();
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  };
};

test('creates conversations and appends trimmed messages', () => {
  let state = createConversation(createEmptyState(), ' Planning ');
  const id = state.activeConversationId;

  state = addMessage(state, id, 'user', '  Hello there  ');

  assert.equal(state.conversations[0].title, 'Planning');
  assert.equal(state.conversations[0].messages.length, 1);
  assert.equal(state.conversations[0].messages[0].content, 'Hello there');
});

test('renames and deletes the active conversation', () => {
  let state = createConversation(createEmptyState(), 'First');
  const firstId = state.activeConversationId;
  state = createConversation(state, 'Second');
  const secondId = state.activeConversationId;

  state = renameConversation(state, secondId, 'Second draft');
  assert.equal(state.conversations[0].title, 'Second draft');

  state = deleteConversation(state, secondId);
  assert.equal(state.activeConversationId, firstId);
  assert.equal(state.conversations.length, 1);
});

test('persists and restores conversations from storage', () => {
  const storage = createMemoryStorage();
  let state = createConversation(createEmptyState(), 'Saved');
  state = addMessage(state, state.activeConversationId, 'note', 'Remember this');

  saveState(state, storage);
  const restored = loadState(storage);

  assert.equal(restored.activeConversationId, state.activeConversationId);
  assert.equal(restored.conversations[0].messages[0].content, 'Remember this');
});

test('exports a conversation as markdown', () => {
  let state = createConversation(createEmptyState(), 'Exportable');
  state = addMessage(state, state.activeConversationId, 'assistant', 'Done');

  const markdown = exportConversation(state.conversations[0]);

  assert.match(markdown, /^# Exportable/);
  assert.match(markdown, /\*\*assistant\*\*/);
  assert.match(markdown, /Done/);
});
