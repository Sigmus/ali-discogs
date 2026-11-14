/* Searchable multi-select with native checkbox keyboard behaviour. */
(() => {
  let opened = null;
  class MultiPicker {
    constructor(select) {
      this.select = select;
      this.field = select.parentElement;
      this.field.classList.add('multi-picker');
      this.button = document.createElement('button');
      this.button.type = 'button';
      this.button.id = select.id + '-picker';
      this.button.className = 'multi-trigger';
      this.button.setAttribute('aria-labelledby', select.id + '-label ' + select.id + '-summary');
      this.button.setAttribute('aria-expanded', 'false');
      this.button.setAttribute('aria-controls', select.id + '-menu');
      this.button.innerHTML = `<span id="${select.id}-summary" class="multi-summary"></span><span class="multi-chevron" aria-hidden="true"></span>`;
      this.chips = document.createElement('div');
      this.chips.className = 'multi-chips';
      this.field.append(this.button, this.chips);
      this.button.addEventListener('click', () => this.menu ? this.close() : this.open());
      this.button.addEventListener('keydown', e => { if (e.key === 'ArrowDown') { e.preventDefault(); if (!this.menu) this.open(); else this.search.focus(); } });
      this.refresh();
    }
    options() { return [...this.select.options].filter(o => o.value); }
    selected() { return this.options().filter(o => o.selected); }
    change(value, checked) {
      const option = this.options().find(o => o.value === value);
      if (option) option.selected = checked;
      this.select.dispatchEvent(new Event('change', { bubbles: true }));
    }
    refresh() {
      const selected = this.selected();
      this.button.querySelector('.multi-summary').textContent = selected.length ? `${selected.length} selected` : this.select.dataset.placeholder;
      this.chips.replaceChildren();
      selected.forEach(option => {
        const chip = document.createElement('button');
        chip.type = 'button'; chip.className = 'multi-chip';
        const name = option.textContent.replace(/ \(\d+\)$/, '');
        chip.textContent = name + ' ×'; chip.title = name;
        chip.setAttribute('aria-label', 'Remove ' + name);
        chip.addEventListener('click', () => { this.change(option.value, false); this.button.focus(); });
        this.chips.append(chip);
      });
      if (this.menu) {
        this.footerCount.textContent = `${selected.length} selected`;
        this.list.querySelectorAll('input').forEach(input => input.checked = selected.some(o => o.value === input.value));
        this.position();
      }
    }
    renderOptions() {
      const query = this.search.value.toLocaleLowerCase();
      this.list.replaceChildren();
      this.options().filter(o => o.textContent.toLocaleLowerCase().includes(query)).forEach(option => {
        const row = document.createElement('label'); row.className = 'multi-option';
        const box = document.createElement('input'); box.type = 'checkbox'; box.value = option.value; box.checked = option.selected;
        const name = document.createElement('span'); name.className = 'multi-option-name'; name.textContent = option.textContent.replace(/ \(\d+\)$/, '');
        const count = document.createElement('span'); count.className = 'multi-option-count'; count.textContent = option.textContent.match(/\((\d+)\)$/)?.[1] || '';
        row.append(box, name, count);
        box.addEventListener('change', () => this.change(option.value, box.checked));
        this.list.append(row);
      });
      if (!this.list.children.length) { const empty = document.createElement('p'); empty.className = 'multi-empty'; empty.textContent = 'No options match your search.'; this.list.append(empty); }
    }
    position() {
      const rect = this.button.getBoundingClientRect();
      const width = Math.min(Math.max(rect.width, 300), innerWidth - 24);
      this.menu.style.width = width + 'px';
      this.menu.style.left = Math.max(12, Math.min(rect.left, innerWidth - width - 12)) + 'px';
      const below = innerHeight - rect.bottom - 12;
      const above = rect.top - 12;
      const upwards = below < 230 && above > below;
      this.menu.style.top = upwards ? 'auto' : (rect.bottom + 6) + 'px';
      this.menu.style.bottom = upwards ? (innerHeight - rect.top + 6) + 'px' : 'auto';
      this.list.style.maxHeight = Math.max(70, Math.min(260, (upwards ? above : below) - 108)) + 'px';
    }
    open() {
      if (opened) opened.close(); opened = this;
      this.menu = document.createElement('div'); this.menu.className = 'multi-menu'; this.menu.id = this.select.id + '-menu';
      this.menu.setAttribute('role', 'group'); this.menu.setAttribute('aria-labelledby', this.select.id + '-label');
      this.search = document.createElement('input'); this.search.type = 'search'; this.search.className = 'multi-search';
      this.search.placeholder = 'Search ' + document.getElementById(this.select.id + '-label').textContent.toLowerCase();
      this.search.setAttribute('aria-label', this.search.placeholder);
      this.list = document.createElement('div'); this.list.className = 'multi-options';
      const foot = document.createElement('div'); foot.className = 'multi-footer';
      this.footerCount = document.createElement('span'); this.footerCount.setAttribute('aria-live', 'polite');
      const clear = document.createElement('button'); clear.type = 'button'; clear.textContent = 'Clear selection';
      clear.addEventListener('click', () => { this.options().forEach(o => o.selected = false); this.select.dispatchEvent(new Event('change', { bubbles: true })); });
      foot.append(this.footerCount, clear); this.menu.append(this.search, this.list, foot); document.body.append(this.menu);
      this.search.addEventListener('input', () => this.renderOptions());
      this.menu.addEventListener('keydown', e => {
        if (e.key === 'Escape') { e.preventDefault(); this.close(true); }
        if (e.key === 'ArrowDown' && e.target === this.search) { e.preventDefault(); this.list.querySelector('input')?.focus(); }
      });
      this.renderOptions(); this.refresh(); this.button.setAttribute('aria-expanded', 'true'); this.search.focus();
    }
    close(focus = false) {
      this.menu?.remove(); this.menu = null; this.button.setAttribute('aria-expanded', 'false');
      if (opened === this) opened = null; if (focus) this.button.focus();
    }
  }
  document.addEventListener('pointerdown', e => { if (opened && !opened.menu.contains(e.target) && !opened.field.contains(e.target)) opened.close(); });
  document.addEventListener('focusin', e => { if (opened && !opened.menu.contains(e.target) && !opened.field.contains(e.target)) opened.close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && opened) opened.close(true); });
  window.addEventListener('resize', () => opened?.position());
  window.addEventListener('scroll', e => { if (opened && !opened.menu.contains(e.target)) opened.position(); }, true);
  window.MultiPicker = MultiPicker;
})();
