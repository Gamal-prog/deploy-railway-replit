document.addEventListener("alpine:init", () => {
    const Alpine = window.Alpine;

    Alpine.store("theme", {
        darkModePreference: "system",
        isDarkModeActive: false,
        useLocalStorage: true,
        localStorageKey: "dark-mode",
        mediaQuery: null,
        init() {
            if (this.useLocalStorage) {
                this.darkModePreference = this.loadDarkModePreference();
            }

            this.applyDarkMode();
            this.mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
            const onSystemThemeChange = () => {
                if (this.darkModePreference === "system") {
                    this.applyDarkMode();
                }
            };

            if (typeof this.mediaQuery.addEventListener === "function") {
                this.mediaQuery.addEventListener("change", onSystemThemeChange);
            } else {
                this.mediaQuery.addListener(onSystemThemeChange);
            }
        },
        loadDarkModePreference() {
            try {
                const stored = localStorage.getItem(this.localStorageKey);
                if (stored === "on" || stored === "off" || stored === "system") {
                    return stored;
                }
            } catch (error) {
                // Local storage can be unavailable in private browsing modes.
            }
            return this.darkModePreference;
        },
        isDark() {
            if (this.darkModePreference === "system") {
                return window.matchMedia("(prefers-color-scheme: dark)").matches;
            }
            return this.darkModePreference === "on";
        },
        applyDarkMode() {
            this.isDarkModeActive = this.isDark();
            document.documentElement.classList.toggle("dark", this.isDarkModeActive);
            document.documentElement.classList.toggle("initial-dark", this.isDarkModeActive);
        },
        setDarkMode(value) {
            if (!["on", "off", "system"].includes(value)) {
                return;
            }

            this.darkModePreference = value;
            if (this.useLocalStorage) {
                try {
                    localStorage.setItem(this.localStorageKey, value);
                } catch (error) {
                    // Theme persistence is optional.
                }
            }
            this.applyDarkMode();
        },
        toggle() {
            this.setDarkMode(this.isDarkModeActive ? "off" : "on");
        },
        currentThemeLabel() {
            if (this.darkModePreference === "on") return "Тёмная";
            if (this.darkModePreference === "off") return "Светлая";
            return "Системная";
        },
        isSelected(value) {
            return this.darkModePreference === value;
        },
    });

    Alpine.data("lectureselect", (currentVideo, name, description) => ({
        currentVideo,
        name,
        description,
        select(nextVideo, nextName, nextDescription) {
            this.currentVideo = nextVideo;
            this.name = nextName;
            this.description = nextDescription;
        },
    }));

    Alpine.data("navbar", () => ({
        mobilenavOpen: false,
        open() {
            this.mobilenavOpen = !this.mobilenavOpen;
        },
    }));

    Alpine.data("accordion", () => ({
        activeAccordion: "",
        setActiveAccordion(id) {
            this.activeAccordion = this.activeAccordion === id ? "" : id;
        },
    }));

    Alpine.data("slideover", () => ({
        slideOverOpen: false,
        toggleSlide() {
            this.slideOverOpen = !this.slideOverOpen;
        },
    }));
});
