describe("Header look not logged in", () => {
  it("App name in header", () => {
    cy.visit("/");
    cy.get("header").contains("Peristerónas");
  });
  it("Login in header", () => {
    cy.visit("/");
    cy.get("header").contains("Login");
  });
  it("Language in header", () => {
    cy.visit("/");
    cy.get("header").contains("en");
  });
});

describe("Header functionality not logged in", () => {
  it("Header Login", () => {
    cy.visit("/");
    cy.contains("Login")
      .should("be.visible")
      .should("have.attr", "href")
      .and("include", "login.microsoftonline.com");
  });

  it("Header change language en -> nl", () => {
    cy.visit("/");
    cy.contains("en").should("be.visible").click();
    cy.contains("Nederlands").should("be.visible").click();
    cy.contains("nl").should("be.visible");
  });
});
