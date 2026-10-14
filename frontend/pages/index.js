const Home = ({ prompts }) => {
  const [q, setQ] = React.useState("");
  const [items, setItems] = React.useState(prompts || []);

  const search = async () => {
    const res = await fetch(`/api/proxy/prompts?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    setItems(data);
  };

  return (
    React.createElement('div', { style: { padding: 20 } },
      React.createElement('h1', null, 'Remix Hub — MVP'),
      React.createElement('div', null,
        React.createElement('input', { value: q, onChange: e => setQ(e.target.value), placeholder: 'Search (e.g. котик)' }),
        React.createElement('button', { onClick: search }, 'Search')
      ),
      React.createElement('ul', null, items.map(p => React.createElement('li', { key: p.id }, React.createElement('a', { href: `/prompt/${p.id}` }, p.title))))
    )
  );
}

Home.getInitialProps = async () => {
  try {
    const res = await fetch('http://localhost:8000/prompts');
    const data = await res.json();
    return { prompts: data };
  } catch (e) {
    return { prompts: [] };
  }
}

export default Home;
