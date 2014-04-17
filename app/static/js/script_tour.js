(function(){

    var tour = new Tour({
        storage : false
    });

    tour.addSteps([
      {
        element: ".tour-step.tour-step-zero",
        placement: "bottom",
        title: "Quitter",
        content: "Arrétez la démo et revenez à votre PROFIL"
      },
      {
        element: ".tour-step.tour-step-one",
        placement: "bottom",
        title: "Bienvenu sur l'espace de DEMO de l'APIClock",
        content: "Ce menu vous propose d'accéder à la gestion de vos podcast"
      },

    ]);

    // Initialize the tour
    tour.init();

    // Start the tour
    tour.start();

}());