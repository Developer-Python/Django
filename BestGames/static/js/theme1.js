var navigation = {
    // Variables
    $navTrigger: document.querySelector('.nav__trigger'),
    $nav: document.querySelector('.nav'),
    //$navItems: document.querySelectorAll('.nav__item a'),
    $main: document.querySelector('.main'),
    transitionEnd: 'webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
    isOpeningNav: false,

    init: function init() {
        var self = this;

        // Reset overflow and height on load
        self.$main.style.overflow = 'auto';

        // Handle scroll events
        window.addEventListener('scroll', function (e) {
            if (window.scrollY == 0 && self.isOpeningNav) {
                self.isOpeningNav = false;

                // Add a small delay
                setTimeout(function () {
                    self.openNavigation();
                }, 150);
            }
        });

        // Handle .nav__trigger click event
        self.$navTrigger.addEventListener('click', function (e) {
            e.preventDefault();

            if (!self.$navTrigger.classList.contains('is-active')) {
                if (window.scrollY !== 0) {
                    // Scroll to top
                    window.scroll({ top: 0, left: 0, behavior: 'smooth' });

                    // Enable opening nav
                    self.isOpeningNav = true;
                } else {
                    self.openNavigation();
                }
            } else {
                self.closeNavigation();
            }
        });

        // Handle .nav__item click events
        self.$navItems.forEach(function (navLink) {
            navLink.addEventListener('click', function (e) {
                e.preventDefault();

                // Remove is-active from all .nav__items
                self.$navItems.forEach(function (el) {
                    el.classList.remove('is-active');
                });

                // Ad is-active to clicked .nav__item
                this.classList.add('is-active');

                // Transition the page
                self.transitionPage();
            });
        });
    },
    openNavigation: function openNavigation() {
        var self = this;

        // .nav--trigger active
        self.$navTrigger.classList.add('is-active');

        // body froze
        document.body.classList.add('is-froze');

        // Remove old inline styles
        if (self.$main.style.removeProperty) {
            self.$main.style.removeProperty('overflow');
            self.$main.style.removeProperty('height');
        } else {
            self.$main.style.removeAttribute('overflow');
            self.$main.style.removeAttribute('height');
        }

        // .main active
        self.$main.classList.add('is-active');
    },
    closeNavigation: function closeNavigation() {
        var self = this;

        // .nav--trigger inactive
        self.$navTrigger.classList.remove('is-active');

        // .main inactive
        self.$main.classList.remove('is-active');
        self.$main.addEventListener('transitionend', function (e) {
            if (e.propertyName == 'transform' && !self.$navTrigger.classList.contains('is-active')) {
                // Reset overflow and height
                self.$main.style.overflow = 'auto';

                // body unfroze
                document.body.classList.remove('is-froze');
            }
        });

        // no-csstransitions fallback
        if (document.documentElement.classList.contains('no-csstransitions')) {
            // .main inactive
            self.$main.classList.remove('is-active');

            // body unfroze
            document.body.classList.remove('is-froze');
        }
    },
    transitionPage: function transitionPage() {
        var self = this;

        // .main transitioning
        self.$main.classList.add('is-transition-out');
        self.$main.addEventListener('transitionend', function (e) {
            if (e.propertyName == 'clip-path') {
                if (self.$main.classList.contains('is-transition-in')) {
                    self.$main.classList.remove('is-transition-in');
                    self.$main.classList.remove('is-transition-out');
                    self.closeNavigation();
                }

                if (self.$main.classList.contains('is-transition-out')) {
                    self.$main.classList.remove('is-transition-out');

                    // Add new content to .main

                    setTimeout(function () {
                        self.$main.classList.add('is-transition-in');
                    }, 500);
                }
            }
        });
    }
};

navigation.init();