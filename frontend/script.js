document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const backToTopButton = document.getElementById('back-to-top');

    hamburger.addEventListener('click', (e) => {
        e.stopPropagation();
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close menu when a link is clicked or clicking outside
    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active') && !navLinks.contains(e.target) && !hamburger.contains(e.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });

    // Smooth scrolling for anchor links, excluding links that just have "#"
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Ensure it's a valid on-page link
            if (document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu after clicking a link
                if (navLinks.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    navLinks.classList.remove('active');
                }
            }
        });
    });

    // Scroll animations
    const animatedElements = document.querySelectorAll('.animated');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(el => {
        observer.observe(el);
    });

    // Back to top button visibility
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            if (backToTopButton.style.display !== 'block') {
                backToTopButton.style.display = 'block';
                setTimeout(() => {
                    backToTopButton.style.opacity = '1';
                    backToTopButton.style.transform = 'translateY(0)';
                }, 10);
            }
        } else {
            if (backToTopButton.style.display === 'block') {
                backToTopButton.style.opacity = '0';
                backToTopButton.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    backToTopButton.style.display = 'none';
                }, 300);
            }
        }
    });

    // Modal logic
    const modal = document.getElementById('email-modal');
    if (modal) {
        const downloadBtns = document.querySelectorAll('.download-btn');
        const closeBtn = document.querySelector('.close-button');
        const emailForm = document.getElementById('email-form');
        let requestedPdfPath = '';

        downloadBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                requestedPdfPath = btn.getAttribute('data-pdf');
                modal.style.display = 'block';
            });
        });

        const closeModal = () => {
            modal.style.display = 'none';
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', closeModal);
        }

        window.addEventListener('click', (e) => {
            if (e.target == modal) {
                closeModal();
            }
        });

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'block') {
                closeModal();
            }
        });

        if (emailForm) {
            emailForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const email = document.getElementById('email-input').value;
                console.log(`Email submitted: ${email}. Preparing to download ${requestedPdfPath}`);
                
                // Simulate sending email and then trigger download
                alert(`Thank you! The download will begin shortly.`);

                // Create a temporary link to trigger the download
                const link = document.createElement('a');
                link.href = requestedPdfPath;
                link.download = requestedPdfPath.split('/').pop();
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                closeModal();
                emailForm.reset();
            });
        }
    }
});