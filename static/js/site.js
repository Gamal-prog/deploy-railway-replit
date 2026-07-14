(() => {
    const root = document.documentElement;
    const storageKey = "lecturelib-theme";
    const button = document.querySelector("[data-theme-toggle]");
    const icon = document.querySelector("[data-theme-icon]");

    const prefersDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;
    const storedTheme = () => {
        try {
            return localStorage.getItem(storageKey);
        } catch (error) {
            return null;
        }
    };

    const resolveTheme = () => storedTheme() || (prefersDark() ? "dark" : "light");

    const applyTheme = (theme) => {
        root.dataset.theme = theme;
        if (icon) {
            icon.textContent = theme === "dark" ? "☀" : "☾";
        }
    };

    applyTheme(resolveTheme());

    if (button) {
        button.addEventListener("click", () => {
            const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
            try {
                localStorage.setItem(storageKey, nextTheme);
            } catch (error) {
                // Theme persistence is optional.
            }
            applyTheme(nextTheme);
        });
    }
})();
