import React from 'react';

const Create = () => {
  const [title, setTitle] = React.useState('');
  const [body, setBody] = React.useState('');
  const create = async () => {
    await fetch('http://localhost:8000/prompts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, body })
    });
    alert('Created (may be anonymous). Reload list.');
  };
  return (
    React.createElement('div', { style: { padding: 20 } },
      React.createElement('h1', null, 'Create / Remix Prompt'),
      React.createElement('input', { placeholder: 'Title', value: title, onChange: e => setTitle(e.target.value) }),
      React.createElement('br'),
      React.createElement('textarea', { placeholder: 'Body', value: body, onChange: e => setBody(e.target.value), rows: 10, cols: 60 }),
      React.createElement('br'),
      React.createElement('button', { onClick: create }, 'Create')
    )
  );
}
export default Create;
