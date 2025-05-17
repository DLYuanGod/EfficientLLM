document.addEventListener('DOMContentLoaded', function() {
  const table = document.getElementById('efficiency-table');
  if (!table) return;
  
  // 筛选功能
  const filterButtons = document.querySelectorAll('[data-filter]');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // 移除所有按钮的active类
      filterButtons.forEach(btn => btn.classList.remove('active'));
      // 添加当前按钮的active类
      this.classList.add('active');
      
      const filter = this.getAttribute('data-filter');
      const rows = table.querySelectorAll('tbody tr');
      
      rows.forEach(row => {
        if (filter === 'all') {
          row.style.display = '';
        } else {
          const category = row.getAttribute('data-category');
          row.style.display = (category === filter) ? '' : 'none';
        }
      });
    });
  });
  
  // 排序功能
  const sortIcons = document.querySelectorAll('.sort-icon');
  
  sortIcons.forEach(icon => {
    icon.addEventListener('click', function() {
      const sortBy = this.getAttribute('data-sort');
      const columnIndex = this.closest('th').cellIndex;
      
      // 移除所有排序图标的active类
      sortIcons.forEach(i => i.classList.remove('active'));
      // 添加当前排序图标的active类
      this.classList.add('active');
      
      // 切换排序方向
      const isAscending = !this.classList.contains('desc');
      
      if (isAscending) {
        this.classList.add('desc');
      } else {
        this.classList.remove('desc');
      }
      
      // 获取所有行
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr:not([data-subcategory])'));
      
      // 排序行
      rows.sort((a, b) => {
        // 获取单元格的值
        const aValue = a.children[columnIndex] ? parseInt(a.children[columnIndex].textContent) || 0 : 0;
        const bValue = b.children[columnIndex] ? parseInt(b.children[columnIndex].textContent) || 0 : 0;
        
        // 比较值
        if (isAscending) {
          return aValue - bValue;
        } else {
          return bValue - aValue;
        }
      });
      
      // 移除旧的行
      const rowGroups = new Map();
      const allRows = Array.from(tbody.querySelectorAll('tr'));
      
      // 分组行
      allRows.forEach(row => {
        const category = row.getAttribute('data-subcategory');
        if (category) {
          if (!rowGroups.has(category)) {
            rowGroups.set(category, []);
          }
          rowGroups.get(category).push(row);
        }
      });
      
      // 清空表格
      while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
      }
      
      // 按排序顺序重新添加行
      rows.forEach(row => {
        const category = row.getAttribute('data-subcategory');
        tbody.appendChild(row);
        
        // 添加相同类别的行
        if (category && rowGroups.has(category)) {
          rowGroups.get(category).forEach(subRow => {
            if (subRow !== row) {
              tbody.appendChild(subRow);
            }
          });
        }
      });
    });
  });
  
  // 行高亮效果
  const tableRows = table.querySelectorAll('tbody tr');
  tableRows.forEach(row => {
    row.addEventListener('mouseenter', function() {
      this.classList.add('highlight');
    });
    row.addEventListener('mouseleave', function() {
      this.classList.remove('highlight');
    });
  });
  
  // 表格响应式调整
  function adjustTable() {
    const windowWidth = window.innerWidth;
    if (windowWidth < 768) {
      table.classList.add('table-sm');
    } else {
      table.classList.remove('table-sm');
    }
  }
  
  // 初始调整和窗口大小变化时调整
  adjustTable();
  window.addEventListener('resize', adjustTable);
}); 