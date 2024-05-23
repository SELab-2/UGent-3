// e2e needs to check that you can actually go from certain page to other pages using navbar/header
// also logout and maybe changing language? (how to test language stuff?)
// component tests that everything is present that has to be present
import me from "../../tests/utils/me-fixture.ts";

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
    // good enough test, will need to test validity of url some other way because can't really login if we can't make our own account for testing
  });

  it("Header change language en -> nl", () => {
    cy.visit("/");
    cy.contains("en").should("be.visible").click();
    cy.contains("Nederlands").should("be.visible").click();
    cy.contains("nl").should("be.visible");
  });
});

describe("Header functionality logged in", () => {
  it("Display name in header", () => {
    const response = {
      statusCode: 200,
      body: me,
    };
    cy.intercept(
      '/me',
      response
    ).as("getMe");
    cy.intercept('/projects', []).as("getProjects");
    cy.log(response);
    cy.visit("/en/home");
    cy.wait("@getMe");
    cy.wait("@getProjects");
  });
});
