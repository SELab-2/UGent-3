describe("Homepage not logged in functionality", () => {
  it("Header Visible", () => {
    cy.visit("http://localhost:5173");
    cy.contains("Peristerónas");
    cy.get("header").should("be.visible");
  });

  it("Center button Login", () => {
    cy.visit("http://localhost:5173");
    cy.contains("Peristerónas");
    cy.get(
      "a.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.css-sghohy-MuiButtonBase-root-MuiButton-root"
    )
      .eq(1)
      .contains("Login")
      .should("be.visible")
      .should("have.attr", "href")
      .and("include", "login.microsoftonline.com");
  });
});
