// google analytics tack mailto clicks
(function() {
  function addEventListener(element, listener) {
    // for IE8 compatibility
    if (element.addEventListener) {
      element.addEventListener('click', listener, false);
    } else {
      element.attachEvent('onclick', listener);
    }
  }
  function trackMailtoLinkClick(event) {
    ga('send', 'event', {
      eventCategory: 'Mailto link',
      eventAction: 'click',
      eventLabel: event.target.href,
    });
  }
  var mailToElementSelector = '.js-track-mailto-click';
  var elements = document.querySelectorAll(mailToElementSelector);
  for (var i=0, element; element = elements[i]; i++) {
    addEventListener(element, trackMailtoLinkClick)
  }
})();
