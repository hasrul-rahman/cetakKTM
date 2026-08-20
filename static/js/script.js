// API Base URL
const API_BASE = window.location.origin;
let currentMahasiswa = null;

// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', function() {
        const tabName = this.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Deactivate all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'manage') {
        loadAllMahasiswa();
    }
}

// Search mahasiswa
function searchMahasiswa() {
    const nim = document.getElementById('search-nim').value.trim();
    
    if (!nim) {
        showAlert('Silakan masukkan NIM!', 'error');
        return;
    }
    
    fetch(`${API_BASE}/api/mahasiswa/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nim: nim })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert(data.error, 'error');
            clearForm();
        } else {
            currentMahasiswa = data;
            displayMahasiswa(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat mencari data', 'error');
    });
}

function displayMahasiswa(data) {
    document.getElementById('display-nim').textContent = data.nim;
    document.getElementById('display-nama').textContent = data.nama;
    document.getElementById('display-prodi').textContent = data.prodi;
    document.getElementById('student-data').style.display = 'block';
    document.getElementById('btn-preview').disabled = false;
    document.getElementById('btn-print').disabled = false;
}

// Preview KTM
function previewKTM() {
    if (!currentMahasiswa) {
        showAlert('Silakan cari data mahasiswa terlebih dahulu!', 'error');
        return;
    }
    
    fetch(`${API_BASE}/api/ktm/preview`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentMahasiswa)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        window.open(url, '_blank');
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Gagal membuka preview PDF', 'error');
    });
}

// Download PDF
function downloadPDF() {
    if (!currentMahasiswa) {
        showAlert('Silakan cari data mahasiswa terlebih dahulu!', 'error');
        return;
    }
    
    fetch(`${API_BASE}/api/ktm/generate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentMahasiswa)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `KTM_${currentMahasiswa.nim}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showAlert('KTM berhasil diunduh!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Gagal mengunduh PDF', 'error');
    });
}

// Clear form
function clearForm() {
    document.getElementById('search-nim').value = '';
    document.getElementById('display-nim').textContent = '-';
    document.getElementById('display-nama').textContent = '-';
    document.getElementById('display-prodi').textContent = '-';
    document.getElementById('student-data').style.display = 'none';
    document.getElementById('btn-preview').disabled = true;
    document.getElementById('btn-print').disabled = true;
    currentMahasiswa = null;
}

// Add mahasiswa
function addMahasiswa() {
    const nim = document.getElementById('form-nim').value.trim();
    const nama = document.getElementById('form-nama').value.trim();
    const prodi = document.getElementById('form-prodi').value.trim();
    const tanggal_lahir = document.getElementById('form-tanggal').value;
    
    if (!nim || !nama || !prodi) {
        showAlert('Silakan isi semua field yang wajib!', 'error');
        return;
    }
    
    fetch(`${API_BASE}/api/mahasiswa/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nim: nim,
            nama: nama,
            prodi: prodi,
            tanggal_lahir: tanggal_lahir
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert(data.error, 'error');
        } else {
            showAlert(data.message, 'success');
            clearFormFields();
            loadAllMahasiswa();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat menambah data', 'error');
    });
}

// Clear form fields
function clearFormFields() {
    document.getElementById('form-nim').value = '';
    document.getElementById('form-nama').value = '';
    document.getElementById('form-prodi').value = '';
    document.getElementById('form-tanggal').value = '';
}

// Load all mahasiswa
function loadAllMahasiswa() {
    fetch(`${API_BASE}/api/mahasiswa/all`)
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('table-body');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #999;">Tidak ada data mahasiswa</td></tr>';
            return;
        }
        
        data.forEach(mahasiswa => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${mahasiswa.nim}</td>
                <td>${mahasiswa.nama}</td>
                <td>${mahasiswa.prodi}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="editMahasiswa('${mahasiswa.nim}')">Edit</button>
                        <button class="btn btn-danger" onclick="deleteMahasiswa('${mahasiswa.nim}')">Hapus</button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Gagal memuat data mahasiswa', 'error');
    });
}

// Edit mahasiswa (placeholder)
function editMahasiswa(nim) {
    showAlert('Fitur edit sedang dalam pengembangan', 'info');
}

// Delete mahasiswa
function deleteMahasiswa(nim) {
    if (!confirm(`Apakah Anda yakin ingin menghapus data NIM ${nim}?`)) {
        return;
    }
    
    fetch(`${API_BASE}/api/mahasiswa/delete`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nim: nim })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert(data.error, 'error');
        } else {
            showAlert(data.message, 'success');
            loadAllMahasiswa();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat menghapus data', 'error');
    });
}

// Show alert message
function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    const section = document.querySelector('.section');
    section.insertBefore(alert, section.firstChild);
    
    setTimeout(() => {
        alert.remove();
    }, 4000);
}

// Load data on page load
window.addEventListener('load', () => {
    // Health check
    fetch(`${API_BASE}/health`)
    .catch(error => {
        console.error('Server health check failed:', error);
    });
});
