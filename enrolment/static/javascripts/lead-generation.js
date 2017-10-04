var GOVUK = GOVUK || {}
GOVUK.utils = GOVUK.utils || {};

GOVUK.utils.toggleOtherOnClick = (function() {
  return function toggleOtherOnClick(inputBox, tickboxes) {
    function hide(element) {
      element.style.display = 'none';
    }

    function show(element) {
      element.style.display = 'list-item';
    }

    function hideInputBox() {
      hide(inputBox.parentElement);
      tickboxes.parentElement.style['margin-bottom'] = '40px';
    }

    function showInputBox() {
      show(inputBox.parentElement);
      tickboxes.parentElement.style['margin-bottom'] = 0;
      inputBox.focus();
    }

    function hideInputBoxLabel() {
      hide(inputBox.parentElement.getElementsByTagName('label')[0])
    }

    function handleCheckboxChange(event) {
      if (event.target.checked) {
        showInputBox();
      } else {
        hideInputBox();
        inputBox.value = '';
      }
    }

    if (inputBox.value === '') {
      hideInputBox();
    }
    hideInputBoxLabel();

    var options = tickboxes.getElementsByTagName('input');
    var otherInput = options[options.length -1];
    otherInput.addEventListener('change', handleCheckboxChange);
  };
})();
