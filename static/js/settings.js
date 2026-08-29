document.addEventListener('DOMContentLoaded', () => {
  const bgForm = document.getElementById('bgForm');
  const csvForm = document.getElementById('csvForm');
  const photoForm = document.getElementById('photoForm');

  if (bgForm) {
    bgForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const res = await fetch('/upload-background', { method: 'POST', body: fd });
      const j = await res.json();
      document.getElementById('bgResult').innerText = JSON.stringify(j);
      if (j.ok) location.reload();
    });
  }

  if (csvForm) {
    csvForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const res = await fetch('/bulk-insert', { method: 'POST', body: fd });
      const j = await res.json();
      document.getElementById('csvResult').innerText = JSON.stringify(j, null, 2);
    });
  }

  if (photoForm) {
    photoForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const nim = fd.get('nim').trim();
      if (!nim) { alert('Isi NIM'); return; }
      const res = await fetch('/upload-photo/' + encodeURIComponent(nim), { method: 'POST', body: fd });
      const j = await res.json();
      document.getElementById('photoResult').innerText = JSON.stringify(j, null, 2);
    });
  }
});
