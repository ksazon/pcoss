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
    public class Operations : ControllerBase
    {
        private static readonly object lockA = new object();
        private static readonly object lockB = new object();
        private static readonly object lockC = new object();

        private readonly ILogger<Operations> _logger;

        public Operations(ILogger<Operations> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        [Route("A/{size}")]
        public int GetA(int size)
        {
            lock (lockA)
            {
                Thread.Sleep(size);
                return (new Random()).Next();
            }
        }

        [HttpGet]
        [Route("B/{size}")]
        public int GetB(int size)
        {
            lock (lockB)
            {
                Thread.Sleep(size);
                return (new Random()).Next();
            }
        }

        [HttpGet]
        [Route("C/{size}")]
        public int GetC(int size)
        {
            lock (lockC)
            {
                Thread.Sleep(size);
                return (new Random()).Next();
            }
        }
    }
}
