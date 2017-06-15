var GOVUK = {};

/* 
  General utility methods
  ======================= */
GOVUK.utils = (new function() {

  /* Parse the URL to retrieve a value.
   * @name (String) Name of URL param
   * e.g.
   * GOVUK.utils.getParameterByName('a_param');
   **/
  this.getParameterByName = function(name) {
    var param = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var qs = document.location.search.replace("&amp;", "&");
    var regex = new RegExp("[\\?&]" + param + "=([^&#]*)");
    var results = regex.exec(qs);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  /* Try to dynamically generate a unique String value.
   **/
  this.uniqueString = function() {
    return "_" + ((new Date().getTime()) + "_" + Math.random().toString()).replace(/[^\w]*/mig, "");
  }
});

/*
  Cookie methods
  ==============
  Setting a cookie:
  GOVUK.cookie.set('hobnob', 'tasty', { days: 30 });

  Reading a cookie:
  GOVUK.cookie.get('hobnob');

  Deleting a cookie:
  GOVUK.cookie.set('hobnob', null);
*/
GOVUK.cookie = (new function() {

  /* Set a cookie.
   * @name (String) Name of cookie
   * @value (String) Value to store
   * @options (Object) Optional configurations
   **/
  this.set = function(name, value, options) {
    var opts = options || {};
    var str = name + "=" + value + "; path=/";
    var domain, domainSplit;
    if (opts.days) {
      var date = new Date();
      date.setTime(date.getTime() + (opts.days * 24 * 60 * 60 * 1000));
      str += "; expires=" + date.toGMTString();
    }

    if(opts.domain) {
      str += "; domain=" + opts.domain;
    }

    if (document.location.protocol == 'https:'){
      str += "; Secure";
    }
    
    document.cookie = str;
  }
  
 /* Read a cookie
  * @name (String) Name of cookie to read.
  **/
  this.get = function(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(';');
    var value;

    for(var i = 0, len = cookies.length; i < len; i++) {
      var cookie = cookies[i];
      while (cookie.charAt(0) == ' ') {
        cookie = cookie.substring(1, cookie.length);
      }
      if (cookie.indexOf(nameEQ) === 0) {
        value = decodeURIComponent(cookie.substring(nameEQ.length));
      }
    }
    return value;
  }

  /* Delete a cookie.
   * @name (String) Name of cookie
   **/
  this.remove = function(name) {
    this.set(name, null);
  }

});

/*
  UTM value storage
  =================
  Store values from URL param:
  GOVUK.utm.set();

  Reading stored values:
  GOVUK.utm.get();
*/
GOVUK.utm = (new function() {
  var utils = GOVUK.utils;
  
  this.set = function() {
    // params = [utm_campaign|utm_content|utm_medium|utm_source\utm_term]
    var params = document.location.search.match(/utm_[a-z]+/g) || [];
    var domain = document.getElementById("utmCookieDomain");
    var config = { days: 7 };
    var data = {};
    var json, value;
    
    if(domain) {
      config.domain = domain.getAttribute("value");
    }
    
    // 1. Does not add empty values.
    for(var i=0; i<params.length; ++i) {
      value = utils.getParameterByName(params[i]);
      if(value) {
        data[params[i]] = value;
      }
    }
    
    json = JSON.stringify(data);
    if(json.length > 2) { // ie. not empty
      GOVUK.cookie.set("ed_utm", json, config);
    }
  }

  this.get = function() {
    var cookie = GOVUK.cookie.get("ed_utm");
    return cookie ? JSON.parse(cookie) : null;
  }
  
});


/*
  General reusable component classes
  ==================================== */
GOVUK.components = (new function() {

  /* Attach accessible open and close functionality to an element (e.g. DIV).
   * The toggle functionality only adds CSS "expanded" class so you have full
   * control over actual visual change(s) in stylesheet.
   *
   * @$target (jQuery node) Target element that should toggle
   **/
  this.Expander = Expander;
  function Expander($control, $target) {
    var EXPANDER = this;
    var id = $target.attr("id") || GOVUK.utils.uniqueString("auto_");

    if ($control.length && $target.length) {
      this.$control = Expander.setupControl($control, id);
      this.$target = $target;
      this.$target.attr("id", id);

      this.$control.on("click.Expander", function(e){
        e.preventDefault();
        if(EXPANDER.$target.hasClass("expanded")) {
          EXPANDER.close();
        }
        else {
          EXPANDER.open();
        }
      });
    }
  }
  
  Expander.setupControl = function($control, id) {
    $control.attr("aria-controls", id);
    $control.attr("aria-expanded", "false");
    $control.attr("aria-haspopup", "true");
    $control.attr("tabindex", 0);
    return $control;
  }

  Expander.prototype = {};
  Expander.prototype.open = function() {
    this.$target.addClass("expanded");
    this.$control.attr("aria-expanded", "true");
    $("a", this.$target).eq(0).focus();
  }

  Expander.prototype.close = function(blur) {
    this.$target.removeClass("expanded");
    this.$control.attr("aria-expanded", "false");
  }

});



/* In test mode we don't want the code to 
 * run immediately because we have to compensate
 * for not having a browser environment first.
 **/ 
GOVUK.page = (new function() {
  
  // What to run on every page (called from <body>).
  this.init = function() {
    captureUtmValue();
    addExpanders();
  }
  
  /* Attempt to capture UTM information if we haven't already
   * got something and querystring is not empty.
   **/
  function captureUtmValue() {
    var captured = GOVUK.utm.get();
    if(!captured && document.location.search.substring(1)) {
      GOVUK.utm.set();
    }
  }
  
  /* Setup Accessible Expander component functionality.
   **/
  function addExpanders() {
    var $control = $("#menu-control");
    var $target = $("#menu");
    if($control.length && $target.length) {
      new GOVUK.components.Expander($control, $target);
    }
  }
});




