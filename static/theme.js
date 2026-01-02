(() => {
  const storageKey = "theme";
  const sidebarKey = "sidebar";
  const root = document.documentElement;
  const body = document.body;
  const openDropdowns = () => {
    document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
      dropdown.classList.add("is-open");
    });
  };
  const toggle = () => {
    const current = root.getAttribute("data-theme") || "light";
    const next = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem(storageKey, next);
  };

  const saved = localStorage.getItem(storageKey);
  if (saved) {
    root.setAttribute("data-theme", saved);
  }

  const setSidebarState = (state) => {
    if (!body) {
      return;
    }
    if (state === "collapsed") {
      body.setAttribute("data-sidebar", "collapsed");
    } else {
      body.removeAttribute("data-sidebar");
    }
    document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", state === "collapsed" ? "true" : "false");
    });
  };

  const savedSidebar = localStorage.getItem(sidebarKey);
  if (savedSidebar) {
    setSidebarState(savedSidebar);
  }

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    const button = target.closest("[data-theme-toggle]");
    const sidebarButton = target.closest("[data-sidebar-toggle]");
    if (button) {
      toggle();
    }
    if (sidebarButton) {
      const current = body?.getAttribute("data-sidebar") === "collapsed" ? "collapsed" : "expanded";
      const next = current === "collapsed" ? "expanded" : "collapsed";
      setSidebarState(next);
      localStorage.setItem(sidebarKey, next);
    }
    if (target.closest(".timer-select")) {
      openDropdowns();
    }
    if (target.closest(".timer-list button")) {
      const input = target.closest(".timer-select")?.querySelector("#task-picker");
      if (input) {
        input.value = target.textContent || "";
      }
      document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
        dropdown.classList.remove("is-open");
      });
    }
    if (target.closest(".timer-dropdown") === null && !target.closest(".timer-select")) {
      document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
        dropdown.classList.remove("is-open");
      });
    }
  });
})();
