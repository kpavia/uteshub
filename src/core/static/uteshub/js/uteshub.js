// Utes Hub: click-to-load YouTube. Bootstrap's bundle handles the navbar and dropdown.
// Thumbnails link to YouTube; with JS, the player loads only when clicked,
// so the page doesn't load six iframes up front.

(function () {
  document.addEventListener("click", function (e) {
    var thumb = e.target.closest("[data-youtube-id]");
    if (!thumb || e.metaKey || e.ctrlKey || e.shiftKey) return; // let modified clicks open a tab
    e.preventDefault();
    var id = thumb.getAttribute("data-youtube-id");
    var iframe = document.createElement("iframe");
    iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1";
    iframe.title = thumb.getAttribute("aria-label") || "YouTube video";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    // Django sends Referrer-Policy: same-origin, which strips the referrer YouTube requires.
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.allowFullscreen = true;
    thumb.replaceWith(iframe); // the parent .ratio box sizes it
  });
})();
