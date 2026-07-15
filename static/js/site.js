(() => {
    const root = document.documentElement;
    const storageKey = "lecturelib-theme";
    const button = document.querySelector("[data-theme-toggle]");
    const icon = document.querySelector("[data-theme-icon]");

    const getStoredValue = (key) => {
        try {
            return localStorage.getItem(key);
        } catch (error) {
            return null;
        }
    };

    const storedTheme = () => {
        const portalTheme = getStoredValue(storageKey);
        if (portalTheme === "dark" || portalTheme === "light") {
            return portalTheme;
        }

        return null;
    };

    const resolveTheme = () => storedTheme() || "light";

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
            localStorage.removeItem("dark-mode");
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
