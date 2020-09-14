using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using mgr_server.State;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace mgr_server.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class OperationsController : ControllerBase
    {
        private static readonly object lockA = new object();
        private static readonly object lockB = new object();
        private static readonly object lockC = new object();
        private static readonly object lockD = new object();

        private static ConcurrentDictionary<int, object> lockDict = new ConcurrentDictionary<int, object>(100, 20);

        private readonly ILogger<OperationsController> _logger;
        private OperationsTimes _operationsTimes;

        public OperationsController(ILogger<OperationsController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        [Route("A/{machine}/{input}/{sleep}")]
        public long GetA(int machine, string input, int sleep)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            lock (lockA)
            {
                Thread.Sleep(sleep);
            }
            watch.Stop();
            return watch.ElapsedMilliseconds;
        }

        [HttpGet]
        [Route("B/{machine}/{input}/{sleep}")]
        public long GetB(int machine, string input, int sleep)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            lock (lockB)
            {
                Thread.Sleep(sleep);
            }
            watch.Stop();
            return watch.ElapsedMilliseconds;
        }

        [HttpGet]
        [Route("C/{machine}/{input}/{sleep}")]
        public long GetC(int machine, string input, int sleep)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            lock (lockC)
            {
                Thread.Sleep(sleep);
            }
            watch.Stop();
            
            return watch.ElapsedMilliseconds;
        }

        [HttpGet]
        [Route("D/{machine}/{input}/{sleep}")]
        public long GetD(int machine, string input, int sleep)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            lock (lockD)
            {
                Thread.Sleep(sleep);
            }
            watch.Stop();
            
            return watch.ElapsedMilliseconds;
        }

        [HttpGet]
        [Route("0/{machine}/{input}/{sleep}")]
        public long Get0(int machine, string input, int sleep)
        {
            var watch = System.Diagnostics.Stopwatch.StartNew();
            lockDict.TryAdd(machine, new object());
            lock (lockDict[machine])
            {
                Thread.Sleep(sleep);
            }
            watch.Stop();
            
            return watch.ElapsedMilliseconds;
        }
    }
}
