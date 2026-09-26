using GraveyardGISApp.Data;
using GraveyardGISApp.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace GraveyardGISApp.Controllers
{
    public class ReservationsController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ReservationsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: /Reservations/SearchContacts?q=...
        [HttpGet]
        public IActionResult SearchContacts(string q)
        {
            if (string.IsNullOrWhiteSpace(q) || q.Length < 2)
                return Json(new List<object>());

            var terms = q.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            var query = _context.Contactdetails.AsQueryable();

            foreach (var term in terms)
            {
                var t = term;
                query = query.Where(c =>
                    (c.FirstName != null && c.FirstName.Contains(t)) ||
                    (c.LastName != null && c.LastName.Contains(t)) ||
                    (c.Email != null && c.Email.Contains(t)) ||
                    (c.PhoneNumber != null && c.PhoneNumber.Contains(t)));
            }

            var results = query
                .Select(c => new
                {
                    c.ContactDetailsId,
                    c.FirstName,
                    c.MiddleName,
                    c.LastName,
                    c.PhoneNumber,
                    c.Email,
                    c.Address,
                })
                .Take(10)
                .ToList();

            return Json(results);
        }

        // GET: /Reservations
        public IActionResult Index()
        {
            var plots = (from pd in _context.Plotdetails
                         where pd.PlotStatus == "Reserved"
                         join s in _context.Sections on pd.SectionId equals s.SectionId into sj
                         from s in sj.DefaultIfEmpty()
                         select new ReservationListViewModel
                         {
                             PlotDetailsId = pd.PlotDetailsId,
                             SectionName = s != null ? s.SectionConstant : null,
                             Row = pd.Row,
                         }).ToList();

            var plotIds = plots.Select(x => x.PlotDetailsId).ToList();

            var contacts = (from pcm in _context.Plotcontactmappings
                            where plotIds.Contains(pcm.PlotDetailsId) && pcm.IsPrimaryContact
                            join c in _context.Contactdetails on pcm.ContactDetailsId equals c.ContactDetailsId
                            select new
                            {
                                pcm.PlotContactMappingId,
                                pcm.PlotDetailsId,
                                ContactName = c.FirstName + " " + c.LastName,
                                c.PhoneNumber,
                                ReservedDate = pcm.CreatedDate,
                            })
                           .ToList()
                           .GroupBy(x => x.PlotDetailsId)
                           .ToDictionary(g => g.Key, g => g.OrderByDescending(x => x.PlotContactMappingId).First());

            var payments = (from pay in _context.Paymentdetails
                            join ps in _context.Paymentstatuses on pay.PaymentStatusId equals ps.PaymentStatusId
                            where plotIds.Contains(pay.PlotId)
                            select new
                            {
                                pay.PlotId,
                                pay.PaymentDetailsId,
                                ps.PaymentStatusConstant,
                                pay.BalanceDue,
                                pay.BalancePaid,
                            })
                           .ToList()
                           .GroupBy(x => x.PlotId)
                           .ToDictionary(g => g.Key, g => g.OrderByDescending(x => x.PaymentDetailsId).First());

            foreach (var plot in plots)
            {
                if (contacts.TryGetValue(plot.PlotDetailsId, out var contact))
                {
                    plot.ContactName = contact.ContactName?.Trim();
                    plot.PhoneNumber = contact.PhoneNumber;
                    plot.ReservedDate = contact.ReservedDate;
                }
                if (payments.TryGetValue(plot.PlotDetailsId, out var payment))
                {
                    plot.PaymentStatus = payment.PaymentStatusConstant;
                    plot.BalanceDue = payment.BalanceDue;
                    plot.BalancePaid = payment.BalancePaid;
                }
            }

            return View(plots);
        }

        // GET: /Reservations/Details/5
        public IActionResult Details(int id)
        {
            var plot = (from pd in _context.Plotdetails
                        where pd.PlotDetailsId == id && pd.PlotStatus == "Reserved"
                        join s in _context.Sections on pd.SectionId equals s.SectionId into sj
                        from s in sj.DefaultIfEmpty()
                        select new
                        {
                            pd.PlotDetailsId,
                            pd.Row,
                            pd.Unit,
                            pd.Side,
                            pd.Niche,
                            SectionName = s != null ? s.SectionConstant : null,
                        })
                       .FirstOrDefault();

            if (plot == null) return NotFound();

            var contact = (from pcm in _context.Plotcontactmappings
                           where pcm.PlotDetailsId == id && pcm.IsPrimaryContact
                           join c in _context.Contactdetails on pcm.ContactDetailsId equals c.ContactDetailsId
                           orderby pcm.PlotContactMappingId descending
                           select new
                           {
                               pcm.CreatedDate,
                               c.ContactDetailsId,
                               c.FirstName,
                               c.MiddleName,
                               c.LastName,
                               c.PhoneNumber,
                               c.Email,
                               c.Address,
                           })
                          .FirstOrDefault();

            var payment = (from pay in _context.Paymentdetails
                           where pay.PlotId == id
                           join ps in _context.Paymentstatuses on pay.PaymentStatusId equals ps.PaymentStatusId
                           orderby pay.PaymentDetailsId descending
                           select new
                           {
                               pay.PaymentDetailsId,
                               pay.PaymentStatusId,
                               ps.PaymentStatusConstant,
                               pay.BalanceDue,
                               pay.BalancePaid,
                           })
                          .FirstOrDefault();

            var allStatuses = _context.Paymentstatuses
                .Select(ps => new SelectListItem
                {
                    Value = ps.PaymentStatusId.ToString(),
                    Text = ps.PaymentStatusConstant,
                    Selected = payment != null && ps.PaymentStatusId == payment.PaymentStatusId,
                })
                .ToList();

            var vm = new ReservationDetailViewModel
            {
                PlotDetailsId = plot.PlotDetailsId,
                SectionName = plot.SectionName,
                Row = plot.Row,
                Unit = plot.Unit,
                Side = plot.Side,
                Niche = plot.Niche,

                ContactDetailsId = contact?.ContactDetailsId ?? 0,
                FirstName = contact?.FirstName,
                MiddleName = contact?.MiddleName,
                LastName = contact?.LastName,
                PhoneNumber = contact?.PhoneNumber,
                Email = contact?.Email,
                Address = contact?.Address,
                ReservedDate = contact?.CreatedDate,

                PaymentDetailsId = payment?.PaymentDetailsId,
                PaymentStatusId = payment?.PaymentStatusId,
                PaymentStatusName = payment?.PaymentStatusConstant,
                BalanceDue = payment?.BalanceDue,
                BalancePaid = payment?.BalancePaid,

                AvailablePaymentStatuses = allStatuses,
            };

            return View(vm);
        }

        // POST: /Reservations/Cancel/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Cancel(int id)
        {
            var isReserved = _context.Plotdetails.Any(p => p.PlotDetailsId == id && p.PlotStatus == "Reserved");
            if (!isReserved) return NotFound();

            _context.Plotdetails
                .Where(p => p.PlotDetailsId == id)
                .ExecuteUpdate(s => s
                    .SetProperty(p => p.PlotStatus, "Available")
                    .SetProperty(p => p.IsAvailable, true));

            return RedirectToAction(nameof(Index));
        }

        // POST: /Reservations/UpdatePayment/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult UpdatePayment(int id, int paymentDetailsId, int paymentStatusId, decimal balancePaid)
        {
            var validStatusIds = _context.Paymentstatuses.Select(ps => ps.PaymentStatusId).ToList();
            if (!validStatusIds.Contains(paymentStatusId))
                return BadRequest("Invalid payment status.");

            if (balancePaid < 0)
                return BadRequest("Balance paid cannot be negative.");

            _context.Paymentdetails
                .Where(p => p.PaymentDetailsId == paymentDetailsId && p.PlotId == id)
                .ExecuteUpdate(s => s
                    .SetProperty(p => p.PaymentStatusId, paymentStatusId)
                    .SetProperty(p => p.BalancePaid, balancePaid));

            return RedirectToAction(nameof(Details), new { id });
        }
    }
}
