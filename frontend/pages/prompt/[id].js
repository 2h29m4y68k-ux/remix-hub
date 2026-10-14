import React from 'react';
import { useRouter } from 'next/router';

const PromptView = ({ prompt }) => {
  if (!prompt) return React.createElement('div', null, 'Not found');
  return (
    React.createElement('div', { style: { padding: 20 } },
      React.createElement('h1', null, prompt.title),
      React.createElement('p', null, prompt.description),
      React.createElement('pre', null, prompt.body),
      React.createElement('div', null, React.createElement('a', { href: `/create?parent_id=${prompt.id}` }, 'Remix'))
    )
  );
}

PromptView.getInitialProps = async ({ query }) => {
  const id = query.id;
  try {
    const res = await fetch(`http://localhost:8000/prompts/${id}`);
    const data = await res.json();
    return { prompt: data };
  } catch (e) {
    return { prompt: null };
  }
}

export default PromptView;
