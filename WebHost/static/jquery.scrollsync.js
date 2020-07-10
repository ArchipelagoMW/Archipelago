(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('jquery')) :
      typeof define === 'function' && define.amd ? define(['exports', 'jquery'], factory) :
          (factory((global.$ = global.$ || {}, global.$.fn = global.$.fn || {}), global.$));
}(this, (function (exports, $) {
  'use strict';

  $ = $ && $.hasOwnProperty('default') ? $['default'] : $;

// 参考了（reference）：
// debouncing function from John Hann
// http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
  function debounce(func, threshold) {
    var timeout;
    return function debounced() {
      var obj = this, args = arguments;

      function delayed() {
        // 让调用smartresize的对象执行
        func.apply(obj, args);
        /*
        timeout = null;：这个语句只是单纯将timeout指向null，
        而timeout指向的定时器还存在，
        要想清除定时器（让setTimeout调用的函数不执行）要用clearTimeout(timeout)。
        eg：
        var timeout = setTimeout(function(){
          alert('timeout = null');// 执行
        },1000);
        timeout = null;
        var timeout = setTimeout(function(){
          alert('clearTimeout(timeout)');// 不执行
        },1000);
        clearTimeout(timeout);
        var timeout = setTimeout(function(){
          clearTimeout(timeout);
          alert('clearTimeout(timeout)');// 执行（已经开始执行匿名函数了）
        },1000);
        */
        timeout = null;
      }

      // 如果有timeout正在倒计时，则清除当前timeout
      timeout && clearTimeout(timeout);
      timeout = setTimeout(delayed, threshold || 100);
    };
  }

  function smartscroll(fn, threshold) {
    return fn ? this.bind('scroll', debounce(fn, threshold)) : this.trigger('smartscroll');
  }

//jquery-smartscroll
  $.fn.smartscroll = smartscroll;

  function scrollsync(options) {
    var defaluts = {
      x_sync: true,
      y_sync: true,
      use_smartscroll: false,
      smartscroll_delay: 10,
    };

    // 使用jQuery.extend 覆盖插件默认参数
    var options = $.extend({}, defaluts, options);
    console.log(options);

    var scroll_type = options.use_smartscroll ? 'smartscroll' : 'scroll';
    var $containers = this;

    // 滚动后设置scrolling的值，调用set同步滚动条
    var scrolling = {};
    Object.defineProperty(scrolling, 'top', {
      set: function (val) {
        $containers.each(function () {
          $(this).scrollTop(val);
        });
      }
    });
    Object.defineProperty(scrolling, 'left', {
      set: function (val) {
        $containers.each(function () {
          $(this).scrollLeft(val);
        });
      }
    });

    $containers.on({
      mouseover: function () {
        if (scroll_type == 'smartscroll') {
          $(this).smartscroll(function () {
            options.x_sync && (scrolling.top = $(this).scrollTop());
            options.y_sync && (scrolling.left = $(this).scrollLeft());
          }, options.smartscroll_delay);
          return;
        }
        $(this).bind('scroll', function () {
          options.x_sync && (scrolling.top = $(this).scrollTop());
          options.y_sync && (scrolling.left = $(this).scrollLeft());
        });
      },
      mouseout: function () {
        $(this).unbind('scroll');
      }
    });


    return this;
  }

  exports.scrollsync = scrollsync;

  Object.defineProperty(exports, '__esModule', {value: true});

})));
