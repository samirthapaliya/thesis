$(document).ready(function () {
  $(".customer-bookmark-toggle").click(function (e) {
    e.preventDefault();
    var href = this.href;
    bookmarkButton = $(this).children("i");
    $.ajax({
      url: href,
      success: function (response) {
        if (response["isBookmarked"]) {
          bookmarkButton.removeClass("far");
          bookmarkButton.addClass("fa");
        } else {
          bookmarkButton.removeClass("fa");
          bookmarkButton.addClass("far");
        }
      },
    });
  });
});
