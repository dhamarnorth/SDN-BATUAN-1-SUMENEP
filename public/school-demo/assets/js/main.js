/* =====================================================================
   JavaScript kecil untuk website sekolah.
   1. Menu navbar versi mobile
   2. Sidebar admin versi mobile
   3. Modal konfirmasi sebelum menghapus data
   4. Preview nama file gambar sebelum diunggah
   ===================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  /* 1. Navbar mobile ------------------------------------------------ */
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navbar = document.getElementById("navbar");
  if (navToggle && navbar) {
    navToggle.addEventListener("click", function () {
      navbar.classList.toggle("is-open");
    });
  }

  /* 2. Sidebar admin (mobile) -------------------------------------- */
  const adminToggle = document.querySelector("[data-sidebar-toggle]");
  const shell = document.querySelector(".admin-shell");
  if (adminToggle && shell) {
    adminToggle.addEventListener("click", function () {
      shell.classList.toggle("nav-open");
    });
  }

  /* 3. Modal konfirmasi hapus -------------------------------------- */
  const modal = document.getElementById("konfirmasi-modal");
  const modalText = document.getElementById("konfirmasi-teks");
  const modalForm = document.getElementById("konfirmasi-form");

  function tutupModal() {
    if (modal) modal.classList.remove("is-open");
  }

  // Form hapus selalu memberi atribut data-konfirmasi="..."
  document.querySelectorAll("form[data-konfirmasi]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (form.dataset.dikonfirmasi === "ya") return; // sudah disetujui sekali
      event.preventDefault();
      if (modal && modalForm) {
        modalText.textContent = form.dataset.konfirmasi;
        modalForm.action = form.action;
        modalForm.method = form.method;
        modal.classList.add("is-open");
      }
    });
  });

  document.querySelectorAll("[data-modal-batal]").forEach(function (tombol) {
    tombol.addEventListener("click", tutupModal);
  });

  if (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal) tutupModal();
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") tutupModal();
  });

  // Tombol "Ya, hapus" pada modal
  const modalYa = document.querySelector("[data-modal-ya]");
  if (modalYa && modalForm) {
    modalYa.addEventListener("click", function () {
      modalForm.dataset.dikonfirmasi = "ya";
      modalForm.submit();
    });
  }

  /* 4. Preview nama file gambar ------------------------------------ */
  document.querySelectorAll("input[type=file][data-preview]").forEach(function (input) {
    input.addEventListener("change", function () {
      const target = document.getElementById(input.dataset.preview);
      if (!target) return;
      target.textContent = input.files.length
        ? "Dipilih: " + input.files[0].name
        : "Belum ada file dipilih";
    });
  });

  /* 5. Isi tanggal hari ini bila field tanggal kosong ---------------- */
  const hariIni = new Date().toISOString().slice(0, 10);
  document.querySelectorAll("input[data-tanggal-default]").forEach(function (input) {
    if (!input.value) input.value = hariIni;
  });
});
