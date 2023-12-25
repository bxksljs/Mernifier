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
});
