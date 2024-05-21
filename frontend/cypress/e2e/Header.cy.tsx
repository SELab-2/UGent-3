// e2e needs to check that you can actually go from certain page to other pages using navbar/header
// also logout and maybe changing language? (how to test language stuff?)
// component tests that everything is present that has to be present
describe("Header functionality", () => {
  it("Header Login", () => {
    cy.visit("http://localhost:5173");
    cy.contains("Login")
      .should("be.visible")
      .should("have.attr", "href")
      .and("include", "login.microsoftonline.com");
    // good enough test, will need to test validity of url some other way because can't really login if we can't make our own account for testing
  });
});
