describe("Homepage functionality not logged in ", () => {
  it("Header Visible", () => {
    cy.visit("/");
    cy.contains("Peristerónas");
    cy.get("header").should("be.visible");
  });

  it("Center button Login", () => {
    cy.visit("/");
    cy.contains("Peristerónas");
    cy.get(
      "div.MuiContainer-root.MuiContainer-maxWidthSm.css-cuefkz-MuiContainer-root"
    )
      .contains("Login")
      .should("be.visible")
      .should("have.attr", "href")
      .and("include", "login.microsoftonline.com");
  });
});
