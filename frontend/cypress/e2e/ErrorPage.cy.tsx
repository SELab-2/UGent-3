describe('Error page test', () => {
  it('Error page should load appropriately', () => {
    expect(
      () => {
        cy.request({
          method: 'POST',
          path: '**',
          body: {name: "fail"},
          failOnStatusCode: false
        }).then(response => {
          expect(response.status).to.be(404) // is supposed to be 404
        })
      }
    )
  })
})
