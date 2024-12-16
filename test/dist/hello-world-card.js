class HelloWorldCard extends HTMLElement {

    set hass(hass) {
      // Initialize the content if it's not there yet.
      if (!this.content) {
        this.innerHTML = `
          <ha-card header="Hello">
            <div class="card-content"></div>
          </ha-card>
        `;
        this.content = this.querySelector("div");
      }
  
      this.content.innerHTML = "World!";
    }

    setConfig(config) {
      this.config = config;
    }

    getCardSize() {
      return 1;
    }

    getLayoutOptions() {
      return {
        grid_rows: 1,
        grid_columns: 1,
        grid_min_rows: 1,
        grid_max_rows: 1,
      };
    }
  }
  
  customElements.define("hello-world-card", HelloWorldCard);
