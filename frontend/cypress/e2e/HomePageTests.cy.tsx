describe("Homepage functionality not logged in ", () => {
  it("Header Visible", () => {
    cy.visit("/");
    cy.contains("Peristerónas");
    cy.get("header").should("be.visible");
  });

  it("Center button Login", () => {
    cy.visit("/");
    cy.contains("Peristerónas");
    cy.contains(
      "Welcome to Peristerónas, the online submission platform of UGent"
    )
      .parent()
      .contains("Login")
      .should("be.visible")
      .should("have.attr", "href")
      .and("include", "login.microsoftonline.com");
  });
});
