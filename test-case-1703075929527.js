const chai = require("chai");
const chaiHttp = require("chai-http");
const server = require("../index");
chai.use(chaiHttp);
describe("API tests", () => {
 it("should handle GET request on /test", (done) => {
    chai.request(server)
      .get("/test")
      .end((err, res) => {
        chai.expect(res).to.have.body("GET request received");
        chai.expect(res).to.have.status(200);
        done();
      });
 });
 it("should handle POST request on /test", (done) => {
    chai.request(server)
      .post("/test")
      .end((err, res) => {
        chai.expect(res).to.have.body("POST request received");
        chai.expect(res).to.have.status(200);
        done();
      });
 });
 it("should handle PUT request on /test", (done) => {
    chai.request(server)
      .put("/test")
      .end((err, res) => {
        chai.expect(res).to.have.body("PUT request received");
        chai.expect(res).to.have.status(200);
        done();
      });
 });
 it("should handle DELETE request on /test", (done) => {
    chai.request(server)
      .delete("/test")
      .end((err, res) => {
        chai.expect(res).to.have.body("DELETE request received");
        chai.expect(res).to.have.status(200);
        done();
      });
 });
});
