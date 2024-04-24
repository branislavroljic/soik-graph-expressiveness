function onVisualizerChange(visualizer_id) {
  if (visualizer_id) {
    $.get(
      "/graph/visualizers/" + encodeURIComponent(visualizer_id),
      function (data) {
        location.reload(); // Reloads the current page
      }
    );
  }
}
