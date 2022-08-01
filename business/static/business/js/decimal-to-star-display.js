document.addEventListener("DOMContentLoaded", function () {
  allBusinessRatingsClass = document.querySelectorAll(".overall-rating-display");
  for (var i = 0; i < allBusinessRatingsClass.length; i++) {
    var ratingDecimalClass = allBusinessRatingsClass[i].querySelector(".rating-decimal");
    var ratingInnerStart = allBusinessRatingsClass[i].querySelector(".stars-inner");
    var ratingValue = ratingDecimalClass.innerHTML;
    var starPercentageRounded = getRatings(ratingValue);
    ratingInnerStart.style.width = starPercentageRounded;
  }

  // Get ratings
  function getRatings(ratingValue) {
    var starsTotal = 5;
    // Get percentage
    const starPercentage = (ratingValue / starsTotal) * 100;

    // Round to nearest 10
    const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

    return starPercentageRounded;
  }
  // Get ratings
  function getRatings1() {
    for (let rating in ratings) {
      // Get percentage
      const starPercentage = (ratings[rating] / starsTotal) * 100;

      // Round to nearest 10
      const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

      // Set width of stars-inner to percentage
      document.querySelector(`.${rating} .stars-inner`).style.width = starPercentageRounded;

      // Add number rating
      document.querySelector(`.${rating} .number-rating`).innerHTML = ratings[rating];
    }
  }
});
