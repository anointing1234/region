// =================== ****************** ================== // 
// Template Name: Gadgetize
// Description:  Gadgetize Html Template
// Version: 1.0.0

// =================== ****************** ================== // 

var MyScroll = "";
(function (window, document, $, undefined) {
  "use strict";
  // ==========================================================
  // Detect mobile device and add class "is-mobile" to </body>
  // ==========================================================

  // Detect mobile device (Do not remove!!!)
  var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Nokia|Opera Mini/i.test(navigator.userAgent) ? true : false;
  var Scrollbar = window.Scrollbar;
  // Add class "is-mobile" to </body>

  var Init = {
    i: function (e) {
      Init.s();
      Init.methods();
    },
    s: function (e) {
      (this._window = $(window)),
        (this._document = $(document)),
        (this._body = $("body")),
        (this._html = $("html"));
    },
    methods: function (e) {
      Init.w();
      Init.preloader();
      Init.BackToTop();
      Init.dropdown();
      Init.header();
      Init.slick();
      Init.countdownInit(".countdown", "2025/12/01");
      Init.countryCode();
      Init.filterSearch();
      Init.filterToggle();
      Init.checkBoxes();
      Init.priceRangeSlider();
      Init.billingAddress();
      Init.quantityHandle();
      Init.cartSidebar();
      Init.formValidation();
      Init.contactForm();
    },

    w: function (e) {
      if (isMobile) {
        $("body").addClass("is-mobile");
      }
    },
    preloader: function () {
      setTimeout(function () {
        $("#preloader").hide("slow");
      }, 1800);
    },

    BackToTop: function () {
      var btn = $("#backto-top");
      $(window).on("scroll", function () {
        if ($(window).scrollTop() > 300) {
          btn.addClass("show");
        } else {
          btn.removeClass("show");
        }
      });
      btn.on("click", function (e) {
        e.preventDefault();
        $("html, body").animate(
          {
            scrollTop: 0,
          },
          "300"
        );
      });
    },

    // Header 
    dropdown: function () {
      const selectedAll = document.querySelectorAll(".wrapper-dropdown");

      selectedAll.forEach((selected) => {
        const optionsContainer = selected.children[2];
        const optionsList = selected.querySelectorAll("div.wrapper-dropdown li");

        selected.addEventListener("click", () => {
          let arrow = selected.children[1];

          if (selected.classList.contains("active")) {
            handleDropdown(selected, arrow, false);
          } else {
            let currentActive = document.querySelector(".wrapper-dropdown.active");

            if (currentActive) {
              let anotherArrow = currentActive.children[1];
              handleDropdown(currentActive, anotherArrow, false);
            }

            handleDropdown(selected, arrow, true);
          }
        });

        // update the display of the dropdown
        for (let o of optionsList) {
          o.addEventListener("click", () => {
            selected.querySelector(".selected-display").innerHTML = o.innerHTML;
          });
        }
      });

      // check if anything else ofther than the dropdown is clicked
      window.addEventListener("click", function (e) {
        if (e.target.closest(".wrapper-dropdown") === null) {
          closeAllDropdowns();
        }
      });

      // close all the dropdowns
      function closeAllDropdowns() {
        const selectedAll = document.querySelectorAll(".wrapper-dropdown");
        selectedAll.forEach((selected) => {
          const optionsContainer = selected.children[2];
          let arrow = selected.children[1];

          handleDropdown(selected, arrow, false);
        });
      }

      // open all the dropdowns
      function handleDropdown(dropdown, arrow, open) {
        if (open) {
          arrow.classList.add("rotated");
          dropdown.classList.add("active");
        } else {
          arrow.classList.remove("rotated");
          dropdown.classList.remove("active");
        }
      }

    },

    // Header 
    header: function () {
      function dynamicCurrentMenuClass(selector) {
        let FileName = window.location.href.split("/").reverse()[0];

        selector.find("li").each(function () {
          let anchor = $(this).find("a");
          if ($(anchor).attr("href") == FileName) {
            $(this).addClass("current");
          }
        });
        selector.children("li").each(function () {
          if ($(this).find(".current").length) {
            $(this).addClass("current");
          }
        });
        if ("" == FileName) {
          selector.find("li").eq(0).addClass("current");
        }
      }

      if ($(".main-menu__list").length) {
        let mainNavUL = $(".main-menu__list");
        dynamicCurrentMenuClass(mainNavUL);
      }

      if ($(".main-menu__nav").length && $(".mobile-nav__container").length) {
        let navContent = document.querySelector(".main-menu__nav").innerHTML;
        let mobileNavContainer = document.querySelector(".mobile-nav__container");
        mobileNavContainer.innerHTML = navContent;
      }
      if ($(".sticky-header__content").length) {
        let navContent = document.querySelector(".main-menu").innerHTML;
        let mobileNavContainer = document.querySelector(".sticky-header__content");
        mobileNavContainer.innerHTML = navContent;
      }

      if ($(".mobile-nav__container .main-menu__list").length) {
        let dropdownAnchor = $(
          ".mobile-nav__container .main-menu__list .dropdown > a"
        );
        dropdownAnchor.each(function () {
          let self = $(this);
          let toggleBtn = document.createElement("BUTTON");
          toggleBtn.setAttribute("aria-label", "dropdown toggler");
          toggleBtn.innerHTML = "<i class='fa fa-angle-down'></i>";
          self.append(function () {
            return toggleBtn;
          });
          self.find("button").on("click", function (e) {
            e.preventDefault();
            let self = $(this);
            self.toggleClass("expanded");
            self.parent().toggleClass("expanded");
            self.parent().parent().children("ul").slideToggle();
          });
        });
      }

      if ($(".mobile-nav__toggler").length) {
        $(".mobile-nav__toggler").on("click", function (e) {
          e.preventDefault();
          $(".mobile-nav__wrapper").toggleClass("expanded");
          $("body").toggleClass("locked");
        });
      }

      $(window).on("scroll", function () {
        if ($(".stricked-menu").length) {
          var headerScrollPos = 130;
          var stricky = $(".stricked-menu");
          if ($(window).scrollTop() > headerScrollPos) {
            stricky.addClass("stricky-fixed");
          } else if ($(this).scrollTop() <= headerScrollPos) {
            stricky.removeClass("stricky-fixed");
          }
        }
      });
    },

    // Slick Slider
    slick: function () {
      if ($(".brand-slider").length) {
        $(".brand-slider").slick({
          autoplay: true,
          autoplaySpeed: 0,
          speed: 5000,
          arrows: false,
          swipe: false,
          slidesToShow: 5,
          cssEase: 'linear',
          pauseOnFocus: false,
          pauseOnHover: false,

          responsive: [
            {
              breakpoint: 1025,
              settings: {
                slidesToShow: 4,
              },
            },
            {
              breakpoint: 576,
              settings: {
                slidesToShow: 3,
              },
            },
          ],
        });
      };
      if ($(".blog-slider").length) {
        $(".blog-slider").slick({
          slidesToShow: 4,
          slidesToScroll: 1,
          autoplay: true,
          autoplaySpeed: 4000,
          dots: false,
          arrows: false,
          centerPadding: "0",
          cssEase: "linear",

          responsive: [
            {
              breakpoint: 1400,
              settings: {
                slidesToShow: 3,
              },
            },
            {
              breakpoint: 1025,
              settings: {
                slidesToShow: 2,
              },
            },
            {
              breakpoint: 576,
              settings: {
                slidesToShow: 1,
              },
            },
          ],
        });
      };

      if ($(".product-slider").length) {
        $(".product-slider").slick({
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: false,
          fade: true,
          asNavFor: ".product-slider-asnav",
        });
      }
      if ($(".product-slider-asnav").length) {
        $(".product-slider-asnav").slick({
          slidesToShow: 4,
          slidesToScroll: 1,
          asNavFor: ".product-slider",
          dots: false,
          arrows: false,
          centerMode: false,
          variableWidth: true,
          focusOnSelect: true,
        });
      }

      $(".btn-prev").click(function () {
        var $this = $(this).attr("data-slide");
        $('.' + $this).slick("slickPrev");
      });

      $(".btn-next").click(function () {
        var $this = $(this).attr("data-slide");
        $('.' + $this).slick("slickNext");
      });
    },

    // Countdown Timer
    countdownInit: function (countdownSelector, countdownTime, countdown) {
      var eventCounter = $(countdownSelector);
      if (eventCounter.length) {
        eventCounter.countdown(countdownTime, function (e) {
          $(this).html(
            e.strftime(
              '<li><h2>%D</h2><h6>Days</h6></li>\
              <li><h2>%H</h2><h6>Hrs</h6></li>\
              <li><h2>%M</h2><h6>Mins</h6></li>\
              <li><h2>%S</h2><h6>Secs</h6></li>'
            )
          );
        });
      }
    },

    // Countdown Timer
    countryCode: function (countdownSelector, countdownTime, countdown) {
      $(function () {
        var code = "+01 123 456 789"; // Assigning value from model.
        $('#mobile').val(code);
        $('#mobile').intlTelInput({
          autoHideDialCode: true,
          autoPlaceholder: "ON",
          dropdownContainer: document.body,
          formatOnDisplay: true,
          initialCountry: "us",
          placeholderNumberType: "MOBILE",
          preferredCountries: ['us', 'gb', 'in'],
          separateDialCode: true
        });
        $('#btn-submit').on('click', function () {
          var code = $("#mobile").intlTelInput("getSelectedCountryData").dialCode;
          var phoneNumber = $('#mobile').val();
          document.getElementById("code").innerHTML = code;
          document.getElementById("mobile-number").innerHTML = phoneNumber;
        });
      });



    },

    // Blog Search Toggle 
    filterSearch: function () {
      if ($("#searchInput").length) {
        $("#searchInput").on("keyup", function () {
          var value = $(this).val().toLowerCase();
          $(".blogs-block").filter(function () {
            var hasMatch = $(this).find(".blog-title").text().toLowerCase().indexOf(value) > -1;
            $(this).toggle(hasMatch);
          });
        });
      }
    },

    // Filter Toggle Button
    filterToggle: function () {
      if ($('.category-block').length) {
        $(".category-block .title").on("click", function (e) {
          var count = $(this).data('count');
          if ($('.category-block.box-' + count + ' .content-block').is(':visible')) {
            $('.category-block.box-' + count + ' span i').removeClass('fa-horizontal-rule');
            $('.category-block.box-' + count + ' span i').addClass('fa-plus');
            $('.category-block.box-' + count + ' .content-block').hide('slow');

          } else {
            $('.category-block.box-' + count + ' span i').removeClass('fa-plus');
            $('.category-block.box-' + count + ' span i').addClass('fa-horizontal-rule');
            $('.category-block.box-' + count + ' .content-block').show('slow');
          }
        })
      }
      if ($('.toggle-sidebar').length) {
        $('.shop-filter').on('click', function () {
          $('.toggle-sidebar').animate({ left: '0' }, 300);
          $('.overlay').fadeIn(300);
        });

        $('.overlay').on('click', function () {
          $('.toggle-sidebar').animate({ left: '-400px' }, 300);
          $(this).fadeOut(300);
        });
      }
    },

    // Toggle CheckBoxes
    checkBoxes: function () {
      $('.sub-checkboxes').hide();
      $('.arrow-block').click(function () {
        var subCheckboxes = $(this).next('.sub-checkboxes');
        var chevronIcon = $(this).find('i');
        subCheckboxes.slideToggle('fast');
        chevronIcon.toggleClass('fa-chevron-down fa-chevron-up');
      });
      $('.check-block, .sub-check-box').click(function (event) {
        event.stopPropagation();
      });


      if ($('.customer-container').length) {
        $('.signin-button').click(function () {
          $('.sign-form').slideToggle();
        });
      }

    },

    // Form Validation
    priceRangeSlider: function () {
      const priceGap = 1000;

      $(".price-input input").on("input", function () {
        let minPrice = parseInt($(".price-input .input-min").val()),
          maxPrice = parseInt($(".price-input .input-max").val());

        if (maxPrice - minPrice >= priceGap && maxPrice <= $(".range-input .range-max").attr("max")) {
          if ($(this).hasClass("input-min")) {
            $(".range-input .range-min").val(minPrice);
            $(".slider .progress").css("left", (minPrice / $(".range-input .range-min").attr("max")) * 100 + "%");
          } else {
            $(".range-input .range-max").val(maxPrice);
            $(".slider .progress").css("right", 100 - (maxPrice / $(".range-input .range-max").attr("max")) * 100 + "%");
          }
        }
      });

      $(".range-input input").on("input", function () {
        let minVal = parseInt($(".range-input .range-min").val()),
          maxVal = parseInt($(".range-input .range-max").val());

        if (maxVal - minVal < priceGap) {
          if ($(this).hasClass("range-min")) {
            $(".range-input .range-min").val(maxVal - priceGap);
          } else {
            $(".range-input .range-max").val(minVal + priceGap);
          }
        } else {
          $(".price-input .input-min").val(minVal);
          $(".price-input .input-max").val(maxVal);
          $(".slider .progress").css("left", (minVal / $(".range-input .range-min").attr("max")) * 100 + "%");
          $(".slider .progress").css("right", 100 - (maxVal / $(".range-input .range-max").attr("max")) * 100 + "%");
        }
      });

    },

    // CheckOut Same Billing Address
    billingAddress: function () {
      if ($("#shipAddress").length) {
        $('.billing-address').hide();
        $('#shipAddress').change(function () {
          if ($(this).is(':unchecked')) {
            $('.billing-address').hide("slow");
          } else {
            $('.billing-address').show("slow");
          }
        });
      }

      if ($("#open-menu-all").length) {
        $('.all-category-list').hide();

        $('#open-menu-all').on('click', function (event) {
          event.stopPropagation(); // Prevent click from propagating to document

          if ($('.all-category-list').is(':visible')) {
            $('.all-category-list').slideUp("slow");
            $('body').removeClass('sidebar-active');
            $('.all-navigator i').removeClass('fa-times').addClass('fa-bars');
          } else {
            $('.all-category-list').slideDown("slow");
            setTimeout(function () {
              $('body').addClass('sidebar-active');
              $('.all-navigator i').removeClass('fa-bars').addClass('fa-times');
            }, 500);
          }
        });

        $(document).on('click', function () {
          if ($('body').hasClass('sidebar-active')) {
            $('.all-category-list').slideUp("slow");
            $('body').removeClass('sidebar-active');
            $('.all-navigator i').removeClass('fa-times').addClass('fa-bars');
          }
        });

        // Prevent click on the category list from closing it
        $('.all-category-list').on('click', function (event) {
          event.stopPropagation();
        });
      }
    },

    // Quantity Controller
    quantityHandle: function () {
      $(".decrement").on("click", function () {
        var qtyInput = $(this).closest(".quantity-wrap").children(".number");
        var qtyVal = parseInt(qtyInput.val());
        if (qtyVal > 0) {
          qtyInput.val(qtyVal - 1);
        }
      });
      $(".increment").on("click", function () {
        var qtyInput = $(this).closest(".quantity-wrap").children(".number");
        var qtyVal = parseInt(qtyInput.val());
        qtyInput.val(parseInt(qtyVal + 1));
      });
    },

    // Cart Sidebar
    cartSidebar: function () {
      $(".cart-button").on('click', function () {
        $('#sidebar-cart').css('right', '0');
        $('#sidebar-cart-curtain').fadeIn(0).css('display', 'block').animate({ opacity: 1 }, 200);  // Smooth fade in the curtain
      });

      $('.close-popup').on('click', function () {
        $('#sidebar-cart').css('right', '-101%');
        $('#sidebar-cart-curtain').animate({ opacity: 0 }, 200, function () {
          $(this).css('display', 'none');
        });
      });
    },

    // Form Validation
    formValidation: function () {
      if ($(".contact-form").length) {
        $(".contact-form").validate();
      }
    },

    // Contact Form
    contactForm: function () {
      $(".contact-form").on("submit", function (e) {
        e.preventDefault();
        if ($(".contact-form").valid()) {
          var _self = $(this);
          _self
            .closest("div")
            .find('button[type="submit"]')
            .attr("disabled", "disabled");
          var data = $(this).serialize();
          $.ajax({
            url: "./assets/mail/contact.php",
            type: "post",
            dataType: "json",
            data: data,
            success: function (data) {
              $(".contact-form").trigger("reset");
              _self.find('button[type="submit"]').removeAttr("disabled");
              if (data.success) {
                document.getElementById("message").innerHTML =
                  "<h6 class='color-primary mt-3'>Email Sent Successfully</h6>";
              } else {
                document.getElementById("message").innerHTML =
                  "<h6 class='color-primary mt-3'>There is an error</h6>";
              }
              $("#messages").show("slow");
              $("#messages").slideDown("slow");
              setTimeout(function () {
                $("#messages").slideUp("hide");
                $("#messages").hide("slow");
              }, 4000);
            },
          });
        } else {
          return false;
        }
      });
    },
  };

  Init.i();
})(window, document, jQuery);


