(function() {
  var sectorFilterContainer = document.getElementById('id_sectors');
  var sectorFilterInputs = sectorFilterContainer.getElementsByTagName('input');
  var filterList = document.getElementById('ed-search-filters-list');
  var filterButton = document.getElementById('ed-search-filters-container');

  function handleSectorFilterChange(event) {
    event.target.form.submit();
  }

  function handleFilterButtonClick(event) {
    toggleClass(filterButton, 'ed-js-filter-list-mobile-closed');
  }

  function toggleClass(element, className){
      if (!element || !className){
          return;
      }
      var classString = element.className, nameIndex = classString.indexOf(className);
      if (nameIndex == -1) {
          classString += ' ' + className;
      }
      else {
          classString = classString.substr(0, nameIndex) + classString.substr(nameIndex+className.length);
      }
      element.className = classString;
  }

  for (var i = 0; i < sectorFilterInputs.length; i++) {
    sectorFilterInputs[i].addEventListener('change', handleSectorFilterChange);
  }

  filterButton.addEventListener('click', handleFilterButtonClick);
})();
