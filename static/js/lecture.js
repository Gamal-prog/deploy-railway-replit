(() => {
    const storageKey = "dark-mode";
    const allowedPreferences = ["on", "off", "system"];

    const getStoredPreference = () => {
        try {
            const value = localStorage.getItem(storageKey);
            return allowedPreferences.includes(value) ? value : "system";
        } catch (error) {
            return "system";
        }
    };

    const isDarkPreference = (preference) => {
        if (preference === "system") {
            return window.matchMedia("(prefers-color-scheme: dark)").matches;
        }
        return preference === "on";
    };

    const applyThemePreference = (preference) => {
        const nextPreference = allowedPreferences.includes(preference) ? preference : "system";
        try {
            localStorage.setItem(storageKey, nextPreference);
        } catch (error) {
            // Theme persistence is optional.
        }
        const isDarkModeActive = isDarkPreference(nextPreference);
        document.documentElement.classList.toggle("dark", isDarkModeActive);
        document.documentElement.classList.toggle("initial-dark", isDarkModeActive);
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
            this.mediaQuery.addEventListener("change", () => {
                if (this.darkModePreference === "system") {
                    this.applyDarkMode();
                }
            });
        },
        applyDarkMode() {
            this.isDarkModeActive = theme.isDarkPreference(this.darkModePreference);
            document.documentElement.classList.toggle("dark", this.isDarkModeActive);
        },
        setDarkMode(value) {
            theme.applyThemePreference(value);
        },
        toggle() {
            theme.toggleThemePreference();
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
