

function onVisualizerChange(visualizer_id) {
  if (visualizer_id) {
    $.get(
      "/visualizers/" + encodeURIComponent(visualizer_id),
      function (data) {
        location.reload(); // Reloads the current page
      }
    );
  }
}

function filter() {
  var filter_attribute = document.getElementById("filter-attribute-input").value;
  var filter_operator = document.getElementById("filter_operator").value;
  var filter_value = document.getElementById("filter-value-input").value;
  console.log('Search value:');
  if (filter_attribute && filter_operator && filter_value) {
    var url = new URL(window.location.href);
    var params = new URLSearchParams(url.search);
    params.set('filter_value', filter_value);
    params.set('filter_operator', filter_operator);
    params.set('filter_attribute', filter_attribute);
    part_url = "/filter"
    $.ajax({
      url: `${url.origin}${url.pathname}${part_url}?${params.toString()}`,
      type: 'GET',
      success: function (response) {
        //console.log('Search Results:', response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error('Bad filter input');
      }
    });
  }
}

function search() {
  var searchValue = document.getElementById("search-input").value;
  console.log('Search value:');
  if (searchValue) {
    var url = new URL(window.location.href);
    var params = new URLSearchParams(url.search);
    params.set('src', searchValue);
    part_url = "/search"
    $.ajax({
      url: `${url.origin}${url.pathname}${part_url}?${params.toString()}`,
      type: 'GET',
      success: function (response) {
        //console.log('Search Results:', response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        //console.error('Error:', textStatus, errorThrown);
      }
    });
  }
}

function reset() {
  var url = new URL(window.location.href);
  part_url = "/reset"
  $.ajax({
    url: `${url.origin}${url.pathname}${part_url}`,
    type: 'GET',
    success: function (response) {
      location.reload();
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.error('Error:', textStatus, errorThrown);
    }
  });
}

// Modal

document.addEventListener("DOMContentLoaded", () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add("is-active");
  }

  function closeModal($el) {
    $el.classList.remove("is-active");
  }

  function closeAllModals() {
    (document.querySelectorAll(".modal") || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener("click", () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button:not(.is-success)"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllModals();
    }
  });
});
