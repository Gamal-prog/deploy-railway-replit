(() => {
    const root = document.documentElement;
    const playerStorageKey = "dark-mode";
    const portalStorageKey = "lecturelib-theme";
    const allowedPreferences = ["on", "off", "system"];

    const prefersDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;

    const getStoredValue = (key) => {
        try {
            return localStorage.getItem(key);
        } catch (error) {
            return null;
        }
    };

    const getStoredPreference = () => {
        const playerPreference = getStoredValue(playerStorageKey);
        if (playerPreference === "system") return "system";

        const portalPreference = getStoredValue(portalStorageKey);
        if (portalPreference === "dark") return "on";
        if (portalPreference === "light") return "off";

        if (allowedPreferences.includes(playerPreference)) {
            return playerPreference;
        }

        return "system";
    };

    const isDarkPreference = (preference) => {
        if (preference === "system") {
            return prefersDark();
        }
        return preference === "on";
    };

    const persistPreference = (preference, isDarkModeActive) => {
        try {
            localStorage.setItem(playerStorageKey, preference);
            if (preference === "system") {
                localStorage.removeItem(portalStorageKey);
            } else {
                localStorage.setItem(portalStorageKey, isDarkModeActive ? "dark" : "light");
            }
        } catch (error) {
            // Theme persistence is optional.
        }
    };

    const applyThemePreference = (preference, options = {}) => {
        const nextPreference = allowedPreferences.includes(preference) ? preference : "system";
        const isDarkModeActive = isDarkPreference(nextPreference);

        if (options.persist !== false) {
            persistPreference(nextPreference, isDarkModeActive);
        }

        root.classList.toggle("dark", isDarkModeActive);
        root.classList.toggle("initial-dark", isDarkModeActive);
        root.dataset.theme = isDarkModeActive ? "dark" : "light";

        window.dispatchEvent(
            new CustomEvent("lecturelib:theme-change", {
                detail: {
                    preference: nextPreference,
                    isDarkModeActive,
                },
            })
        );
    };

    const toggleThemePreference = () => {
        applyThemePreference(isDarkPreference(getStoredPreference()) ? "off" : "on");
    };

    window.lectureLibTheme = {
        getStoredPreference,
        applyThemePreference,
        toggleThemePreference,
        isDarkPreference,
    };

    document.addEventListener("click", (event) => {
        const choiceButton = event.target.closest("[data-theme-choice]");
        if (choiceButton) {
            applyThemePreference(choiceButton.dataset.themeChoice);
            return;
        }

        const toggleButton = event.target.closest("[data-theme-toggle]");
        if (toggleButton) {
            toggleThemePreference();
        }
    });
})();

document.addEventListener("alpine:init", () => {
    const Alpine = window.Alpine;
    const theme = window.lectureLibTheme;

    Alpine.store("theme", {
        darkModePreference: "system",
        isDarkModeActive: false,
        mediaQuery: null,
        init() {
            this.darkModePreference = theme.getStoredPreference();
            this.applyDarkMode();
            window.addEventListener("lecturelib:theme-change", (event) => {
                this.darkModePreference = event.detail.preference;
                this.isDarkModeActive = event.detail.isDarkModeActive;
            });
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
        isDark() {
            return theme.isDarkPreference(this.darkModePreference);
        },
        applyDarkMode() {
            this.isDarkModeActive = this.isDark();
            document.documentElement.classList.toggle("dark", this.isDarkModeActive);
            document.documentElement.classList.toggle("initial-dark", this.isDarkModeActive);
            document.documentElement.dataset.theme = this.isDarkModeActive ? "dark" : "light";
        },
        setDarkMode(value) {
            theme.applyThemePreference(value);
        },
        toggle() {
            theme.toggleThemePreference();
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
