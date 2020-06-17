using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace mgr_server.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class OperationA : ControllerBase
    {
        private readonly ILogger<OperationA> _logger;

        public OperationA(ILogger<OperationA> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        [Route("{size}")]
        public int Get(int size)
        {
            Thread.Sleep(size);
            return (new Random()).Next();
        }
    }
}
