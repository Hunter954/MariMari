(() => {
  document.querySelectorAll('.bonus-interest-btn').forEach((button) => {
    button.addEventListener('click', async () => {
      const card = button.closest('[data-bonus-id]');
      const bonusId = card.dataset.bonusId;
      await fetch('/api/bonus/interest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bonus_item_id: bonusId, message: 'Interesse enviado pelo front.' })
      });
      button.textContent = 'Interesse enviado';
      button.disabled = true;
    });
  });
})();
