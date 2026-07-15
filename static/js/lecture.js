(() => {
    const root = document.documentElement;
    const storageKey = "lecturelib-theme";

    const getStoredValue = (key) => {
        try {
            return localStorage.getItem(key);
        } catch (error) {
            return null;
        }
    };

    const getStoredTheme = () => {
        const storedTheme = getStoredValue(storageKey);
        return storedTheme === "dark" || storedTheme === "light" ? storedTheme : "light";
    };

    const getStoredPreference = () => {
        return getStoredTheme() === "dark" ? "on" : "off";
    };

    const persistTheme = (theme) => {
        try {
            localStorage.setItem(storageKey, theme);
            localStorage.removeItem("dark-mode");
        } catch (error) {
            // Theme persistence is optional.
        }
    };

    const applyTheme = (theme, options = {}) => {
        const nextTheme = theme === "dark" ? "dark" : "light";
        const isDarkModeActive = nextTheme === "dark";

        if (options.persist !== false) {
            persistTheme(nextTheme);
        }

        root.classList.toggle("dark", isDarkModeActive);
        root.classList.toggle("initial-dark", isDarkModeActive);
        root.dataset.theme = nextTheme;

        window.dispatchEvent(
            new CustomEvent("lecturelib:theme-change", {
                detail: {
                    preference: nextTheme === "dark" ? "on" : "off",
                    isDarkModeActive,
                    theme: nextTheme,
                },
            })
        );
    };

    const applyThemePreference = (preference, options = {}) => {
        applyTheme(preference === "on" ? "dark" : "light", options);
    };

    const toggleThemePreference = () => {
        applyTheme(root.classList.contains("dark") ? "light" : "dark");
    };

    window.lectureLibTheme = {
        getStoredTheme,
        getStoredPreference,
        applyTheme,
        applyThemePreference,
        toggleThemePreference,
        isDarkPreference(preference) {
            return preference === "on";
        },
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
        darkModePreference: "off",
        isDarkModeActive: false,
        init() {
            this.darkModePreference = theme.getStoredPreference();
            this.applyDarkMode();
            window.addEventListener("lecturelib:theme-change", (event) => {
                this.darkModePreference = event.detail.preference;
                this.isDarkModeActive = event.detail.isDarkModeActive;
            });
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
            return "Светлая";
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
