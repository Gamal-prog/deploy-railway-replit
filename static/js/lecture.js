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
            this.mediaQuery.addEventListener("change", () => {
                if (this.darkModePreference === "system") {
                    this.applyDarkMode();
                }
            });
        },
        loadDarkModePreference() {
            const storedPreference = localStorage.getItem(this.localStorageKey);
            if (["on", "off", "system"].includes(storedPreference)) {
                return storedPreference;
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
        },
        setDarkMode(value) {
            if (!["on", "off", "system"].includes(value)) {
                return;
            }
            this.darkModePreference = value;
            if (this.useLocalStorage) {
                localStorage.setItem(this.localStorageKey, value);
            }
            this.applyDarkMode();
        },
        toggle() {
            this.setDarkMode(this.isDarkModeActive ? "off" : "on");
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
