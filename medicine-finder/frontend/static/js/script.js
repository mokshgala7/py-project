document.addEventListener('DOMContentLoaded', function () {

    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('is-open');
            navToggle.setAttribute('aria-expanded', navLinks.classList.contains('is-open'));
        });

        document.addEventListener('click', function (e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('is-open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    const togglePwBtn = document.getElementById('togglePw');
    if (togglePwBtn) {
        togglePwBtn.addEventListener('click', function () {
            const pwInput = document.getElementById('password');
            if (!pwInput) return;
            if (pwInput.type === 'password') {
                pwInput.type = 'text';
                togglePwBtn.textContent = '🙈';
            } else {
                pwInput.type = 'password';
                togglePwBtn.textContent = '👁';
            }
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            let valid = true;

            const email = document.getElementById('email');
            const emailError = document.getElementById('emailError');
            const password = document.getElementById('password');
            const passwordError = document.getElementById('passwordError');

            emailError.textContent = '';
            passwordError.textContent = '';
            email.classList.remove('is-error');
            password.classList.remove('is-error');

            if (!email.value.trim()) {
                emailError.textContent = 'Email is required.';
                email.classList.add('is-error');
                valid = false;
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                emailError.textContent = 'Please enter a valid email address.';
                email.classList.add('is-error');
                valid = false;
            }

            if (!password.value) {
                passwordError.textContent = 'Password is required.';
                password.classList.add('is-error');
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            let valid = true;

            const name = document.getElementById('name');
            const nameError = document.getElementById('nameError');
            const email = document.getElementById('email');
            const emailError = document.getElementById('emailError');
            const password = document.getElementById('password');
            const passwordError = document.getElementById('passwordError');
            const role = document.getElementById('role');
            const roleError = document.getElementById('roleError');

            [nameError, emailError, passwordError, roleError].forEach(el => { if (el) el.textContent = ''; });
            [name, email, password, role].forEach(el => { if (el) el.classList.remove('is-error'); });

            if (!name.value.trim()) {
                nameError.textContent = 'Full name is required.';
                name.classList.add('is-error');
                valid = false;
            }

            if (!email.value.trim()) {
                emailError.textContent = 'Email is required.';
                email.classList.add('is-error');
                valid = false;
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
                emailError.textContent = 'Please enter a valid email address.';
                email.classList.add('is-error');
                valid = false;
            }

            if (!password.value) {
                passwordError.textContent = 'Password is required.';
                password.classList.add('is-error');
                valid = false;
            } else if (password.value.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters.';
                password.classList.add('is-error');
                valid = false;
            }

            if (role && !role.value) {
                roleError.textContent = 'Please select an account type.';
                role.classList.add('is-error');
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }

    const addMedicineForm = document.getElementById('addMedicineForm');
    if (addMedicineForm) {
        addMedicineForm.addEventListener('submit', function (e) {
            let valid = true;

            const medicineName = document.getElementById('medicine_name');
            const medicineNameError = document.getElementById('medicineNameError');
            const quantity = document.getElementById('quantity');
            const quantityError = document.getElementById('quantityError');

            medicineNameError.textContent = '';
            quantityError.textContent = '';
            medicineName.classList.remove('is-error');
            quantity.classList.remove('is-error');

            if (!medicineName.value.trim()) {
                medicineNameError.textContent = 'Medicine name is required.';
                medicineName.classList.add('is-error');
                valid = false;
            }

            if (quantity.value === '' || quantity.value === null) {
                quantityError.textContent = 'Quantity is required.';
                quantity.classList.add('is-error');
                valid = false;
            } else if (parseInt(quantity.value) < 0) {
                quantityError.textContent = 'Quantity cannot be negative.';
                quantity.classList.add('is-error');
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }

    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            const input = document.getElementById('searchInput');
            const error = document.getElementById('searchError');

            error.textContent = '';
            input.classList.remove('is-error');

            if (!input.value.trim()) {
                error.textContent = 'Please enter a medicine name to search.';
                input.classList.add('is-error');
                e.preventDefault();
            }
        });
    }

    const suggestionTags = document.querySelectorAll('.suggestion-tag');
    if (suggestionTags.length) {
        const searchInput = document.getElementById('searchInput');
        suggestionTags.forEach(function (tag) {
            tag.addEventListener('click', function () {
                if (searchInput) {
                    searchInput.value = tag.dataset.term;
                    searchInput.focus();
                }
            });
        });
    }

    const flashMsgs = document.querySelectorAll('.flash');
    flashMsgs.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 500);
        }, 4000);
    });

    function confirmDelete(e) {
        if (!confirm('Are you sure you want to delete this medicine from your inventory?')) {
            e.preventDefault();
            return false;
        }
        return true;
    }

    window.confirmDelete = confirmDelete;

    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach(function (card, index) {
        card.style.animationDelay = (index * 0.07) + 's';
    });

    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(function (input) {
        input.addEventListener('input', function () {
            input.classList.remove('is-error');
            const errorId = input.id + 'Error';
            const errorEl = document.getElementById(errorId);
            if (errorEl) errorEl.textContent = '';
        });
    });
});