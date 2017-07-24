(function() {
  var sectorFilterContainer = document.getElementById('id_sector');
  var sectorFilterInputs = sectorFilterContainer.getElementsByTagName('input');

  function handleSectorFilterChange(event) {
    event.target.form.submit();
  }

  for (var i = 0; i < sectorFilterInputs.length; i++) {
    sectorFilterInputs[i].addEventListener('change', handleSectorFilterChange);
  }
})();
