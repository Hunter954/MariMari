(() => {
  const ctx = window.EPISODE_CONTEXT;
  if (!ctx) return;
  const fill = document.getElementById('progress-fill');
  const label = document.getElementById('progress-label');
  const playBtn = document.getElementById('play-toggle');
  const likeBtn = document.getElementById('like-toggle');
  let current = ctx.initialProgress || 0;
  let playing = false;
  let timer = null;

  const render = () => {
    const pct = ctx.durationSeconds ? Math.min((current / ctx.durationSeconds) * 100, 100) : 0;
    fill.style.width = pct + '%';
    label.textContent = Math.floor(current) + 's';
    playBtn.textContent = playing ? 'Pausar' : (current > 15 ? 'Retomar' : 'Assistir');
  };

  const persist = async () => {
    await fetch('/api/player/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ episode_id: ctx.episodeId, progress_seconds: Math.floor(current) })
    });
  };

  playBtn?.addEventListener('click', () => {
    playing = !playing;
    clearInterval(timer);
    if (playing) {
      timer = setInterval(() => {
        current += 5;
        if (ctx.durationSeconds && current >= ctx.durationSeconds) {
          current = ctx.durationSeconds;
          playing = false;
          clearInterval(timer);
        }
        render();
        persist();
      }, 5000);
    }
    render();
  });

  likeBtn?.addEventListener('click', async () => {
    const res = await fetch('/api/player/like', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ episode_id: ctx.episodeId })
    });
    const data = await res.json();
    likeBtn.dataset.liked = String(data.liked);
    likeBtn.textContent = data.liked ? 'Curtido' : 'Curtir';
  });

  render();
})();
