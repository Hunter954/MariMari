(() => {
  const list = document.getElementById('comment-list');
  const submit = document.getElementById('comment-submit');
  const textarea = document.getElementById('comment-content');
  const wrapper = document.querySelector('.comments-box');
  if (!list || !submit || !textarea || !wrapper) return;
  const episodeId = wrapper.dataset.episodeId;

  submit.addEventListener('click', async () => {
    const content = textarea.value.trim();
    if (!content) return;
    const res = await fetch('/api/comments/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ episode_id: episodeId, content })
    });
    const data = await res.json();
    if (!data.ok) return;
    const article = document.createElement('article');
    article.className = 'comment-item glass-card-soft';
    article.innerHTML = `<div class="comment-head"><strong>${data.comment.author}</strong><span>${data.comment.created_at}</span></div><p>${data.comment.content}</p>`;
    list.prepend(article);
    textarea.value = '';
  });
})();
