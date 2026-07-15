(() => {
    const root = document.documentElement;
    const storageKey = "lecturelib-theme";
    const playerStorageKey = "dark-mode";
    const button = document.querySelector("[data-theme-toggle]");
    const icon = document.querySelector("[data-theme-icon]");

    const prefersDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;
    const getStoredValue = (key) => {
        try {
            return localStorage.getItem(key);
        } catch (error) {
            return null;
        }
    };

    const storedTheme = () => {
        const playerTheme = getStoredValue(playerStorageKey);
        if (playerTheme === "system") return prefersDark() ? "dark" : "light";

        const portalTheme = getStoredValue(storageKey);
        if (portalTheme === "dark" || portalTheme === "light") {
            return portalTheme;
        }

        if (playerTheme === "on") return "dark";
        if (playerTheme === "off") return "light";

        return null;
    };

    const resolveTheme = () => storedTheme() || (prefersDark() ? "dark" : "light");

    const applyTheme = (theme) => {
        root.dataset.theme = theme;
        root.classList.toggle("dark", theme === "dark");
        if (icon) {
            icon.textContent = theme === "dark" ? "☀" : "☾";
        }
    };

    const persistTheme = (theme) => {
        try {
            localStorage.setItem(storageKey, theme);
            localStorage.setItem(playerStorageKey, theme === "dark" ? "on" : "off");
        } catch (error) {
            // Theme persistence is optional.
        }
    };

    applyTheme(resolveTheme());

    if (button) {
        button.addEventListener("click", () => {
            const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
            persistTheme(nextTheme);
            applyTheme(nextTheme);
        });
    }
})();
