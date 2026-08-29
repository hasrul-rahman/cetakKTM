// Configuration
const API_BASE = '/api';
const CURRENT_DATA = {};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupTabNavigation();
    setupFileDragDrop();
    setupColorPicker();
});

// ========== Tab Navigation ==========
function setupTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// ========== Alert System ==========
function showAlert(message, type = 'info') {
    const alertBox = document.getElementById('alertBox');
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    
    setTimeout(() => {
        alertBox.classList.add('hidden');
    }, 5000);
}

// ========== File Handling ==========
function setupFileDragDrop() {
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach(input => {
        const uploadArea = input.closest('.file-upload');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        uploadArea.addEventListener('dragover', () => {
            uploadArea.style.borderColor = '#0056b3';
            uploadArea.style.background = 'rgba(0, 123, 255, 0.1)';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = 'var(--primary-color)';
            uploadArea.style.background = 'rgba(0, 123, 255, 0.02)';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            uploadArea.style.borderColor = 'var(--primary-color)';
            uploadArea.style.background = 'rgba(0, 123, 255, 0.02)';
            
            const files = e.dataTransfer.files;
            input.files = files;
            input.dispatchEvent(new Event('change', { bubbles: true }));
        });
        
        input.addEventListener('change', function() {
            handleFilePreview(this);
        });
    });
}

function handleFilePreview(input) {
    const file = input.files[0];
    if (!file) return;
    
    const fileSize = (file.size / 1024).toFixed(2);
    
    // Image preview
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = input.closest('.file-upload').nextElementSibling;
            if (preview && preview.classList.contains('photo-preview')) {
                preview.classList.remove('hidden');
                preview.querySelector('img').src = e.target.result;
                preview.querySelector('.file-info').textContent = `${file.name} (${fileSize} KB)`;
            } else if (preview && preview.classList.contains('background-preview')) {
                preview.classList.remove('hidden');
                preview.querySelector('img').src = e.target.result;
                preview.querySelector('.file-info').textContent = `${file.name} (${fileSize} KB)`;
            }
        };
        reader.readAsDataURL(file);
    }
}

// ========== Search & Display ==========
async function searchMahasiswa() {
    const nim = document.getElementById('searchNim').value.trim();
    
    if (!nim) {
        showAlert('Masukkan NIM terlebih dahulu', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/mahasiswa/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nim })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Mahasiswa tidak ditemukan', 'error');
            return;
        }
        
        // Store data
        CURRENT_DATA.mahasiswa = data;
        
        // Display data
        const display = document.getElementById('studentDataDisplay');
        display.classList.remove('hidden');
        
        document.getElementById('displayNim').textContent = data.nim;
        document.getElementById('displayNama').textContent = data.nama;
        document.getElementById('displayProdi').textContent = data.prodi;
        document.getElementById('displayTanggalLahir').textContent = data.tanggal_lahir || '-';
        document.getElementById('displayAlamat').textContent = data.alamat || '-';
        
        // Display photo
        const photoImg = document.getElementById('studentPhoto');
        if (data.foto_path) {
            photoImg.src = `/${data.foto_path}`;
            photoImg.style.display = 'block';
        } else {
            photoImg.style.display = 'none';
        }
        
        showAlert('Data mahasiswa ditemukan', 'success');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat mencari data', 'error');
    }
}

// ========== Add Mahasiswa ==========
async function addMahasiswa() {
    const nim = document.getElementById('addNim').value.trim();
    const nama = document.getElementById('addNama').value.trim();
    const prodi = document.getElementById('addProdi').value.trim();
    const tanggal_lahir = document.getElementById('addTanggalLahir').value;
    const alamat = document.getElementById('addAlamat').value.trim();
    
    if (!nim || !nama || !prodi) {
        showAlert('NIM, Nama, dan Prodi harus diisi', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/mahasiswa/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nim, nama, prodi, tanggal_lahir, alamat
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal menambah mahasiswa', 'error');
            return;
        }
        
        showAlert(data.message, 'success');
        document.getElementById('addMahasiswaForm').reset();
        loadAllMahasiswa();
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan', 'error');
    }
}

// ========== Load All Mahasiswa ==========
async function loadAllMahasiswa() {
    try {
        const response = await fetch(`${API_BASE}/mahasiswa/all`);
        const mahasiswaList = await response.json();
        
        const tbody = document.getElementById('mahasiswaTableBody');
        tbody.innerHTML = '';
        
        mahasiswaList.forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${m.nim}</td>
                <td>${m.nama}</td>
                <td>${m.prodi}</td>
                <td>
                    <button class="btn btn-primary table-action-btn" onclick="editMahasiswa('${m.nim}')">Edit</button>
                    <button class="btn btn-danger table-action-btn" onclick="deleteMahasiswa('${m.nim}')">Hapus</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
        showAlert(`Dimuat ${mahasiswaList.length} data mahasiswa`, 'info');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Gagal memuat data', 'error');
    }
}

// ========== Delete Mahasiswa ==========
async function deleteMahasiswa(nim) {
    if (!confirm(`Yakin hapus mahasiswa dengan NIM ${nim}?`)) return;
    
    try {
        const response = await fetch(`${API_BASE}/mahasiswa/delete`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nim })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal menghapus', 'error');
            return;
        }
        
        showAlert(data.message, 'success');
        loadAllMahasiswa();
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan', 'error');
    }
}

// ========== Photo Upload ==========
async function uploadFoto() {
    const nim = document.getElementById('fotoNim').value.trim();
    const file = document.getElementById('fotoFile').files[0];
    
    if (!nim) {
        showAlert('Masukkan NIM terlebih dahulu', 'warning');
        return;
    }
    
    if (!file) {
        showAlert('Pilih file foto terlebih dahulu', 'warning');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('nim', nim);
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/mahasiswa/upload-foto`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal upload foto', 'error');
            return;
        }
        
        showAlert(data.message, 'success');
        document.getElementById('fotoFile').value = '';
        document.getElementById('photoPreview').classList.add('hidden');
        document.getElementById('fotoNim').value = '';
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat upload foto', 'error');
    }
}

// ========== Background Upload ==========
async function uploadBackground() {
    const file = document.getElementById('bgFile').files[0];
    
    if (!file) {
        showAlert('Pilih file background terlebih dahulu', 'warning');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/ktm/upload-background`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal upload background', 'error');
            return;
        }
        
        showAlert(data.message, 'success');
        document.getElementById('bgFile').value = '';
        document.getElementById('bgPreview').classList.add('hidden');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat upload background', 'error');
    }
}

// ========== Color Picker ==========
function setupColorPicker() {
    const colorPicker = document.getElementById('fontColorPicker');
    const colorValue = document.getElementById('colorValue');
    
    colorPicker.addEventListener('change', function() {
        const color = this.value;
        const colorNames = {
            '#000000': 'Hitam',
            '#ffffff': 'Putih',
            '#ff0000': 'Merah',
            '#00ff00': 'Hijau',
            '#0000ff': 'Biru'
        };
        
        colorValue.textContent = (colorNames[color] || 'Kustom') + ' (' + color + ')';
    });
}

async function updateFontColor() {
    const font_color = document.getElementById('fontColorPicker').value;
    
    try {
        const response = await fetch(`${API_BASE}/ktm/font-color`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ font_color })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal mengubah warna', 'error');
            return;
        }
        
        showAlert(data.message, 'success');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan', 'error');
    }
}

// ========== PDF Generation ==========
async function previewKTM() {
    if (!CURRENT_DATA.mahasiswa) {
        showAlert('Tidak ada data mahasiswa', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/ktm/preview`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(CURRENT_DATA.mahasiswa)
        });
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        document.getElementById('pdfFrame').src = url;
        document.getElementById('pdfModal').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Gagal preview PDF', 'error');
    }
}

async function generateKTM() {
    if (!CURRENT_DATA.mahasiswa) {
        showAlert('Tidak ada data mahasiswa', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/ktm/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(CURRENT_DATA.mahasiswa)
        });
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `KTM_${CURRENT_DATA.mahasiswa.nim}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showAlert('PDF berhasil diunduh', 'success');
    } catch (error) {
        console.error('Error:', error);
        showAlert('Gagal generate PDF', 'error');
    }
}

function closePdfModal() {
    document.getElementById('pdfModal').classList.add('hidden');
}

// ========== Excel Import ==========
async function importExcel() {
    const file = document.getElementById('excelFile').files[0];
    
    if (!file) {
        showAlert('Pilih file Excel terlebih dahulu', 'warning');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/mahasiswa/import-excel`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showAlert(data.error || 'Gagal import data', 'error');
            return;
        }
        
        // Show results
        const results = document.getElementById('importResults');
        results.classList.remove('hidden');
        document.getElementById('successCount').textContent = data.success;
        document.getElementById('failedCount').textContent = data.failed;
        
        // Show errors
        const errorsList = document.getElementById('errorsList');
        errorsList.innerHTML = '';
        if (data.errors.length > 0) {
            data.errors.forEach(error => {
                const p = document.createElement('p');
                p.textContent = error;
                errorsList.appendChild(p);
            });
        }
        
        showAlert(`Import selesai: ${data.success} berhasil, ${data.failed} gagal`, 'success');
        document.getElementById('excelFile').value = '';
    } catch (error) {
        console.error('Error:', error);
        showAlert('Terjadi kesalahan saat import', 'error');
    }
}

function downloadTemplate() {
    window.location.href = `${API_BASE}/mahasiswa/import-template`;
}

// ========== Edit Mahasiswa (stub for future implementation) ==========
function editMahasiswa(nim) {
    alert('Fitur edit akan segera ditambahkan');
}
