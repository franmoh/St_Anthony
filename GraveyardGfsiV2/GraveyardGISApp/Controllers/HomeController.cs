using System.Diagnostics;
using GraveyardGISApp.Data;
using GraveyardGISApp.Data.Entities;
using GraveyardGISApp.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace GraveyardGISApp.Controllers
{
    public class HomeController : Controller
    {
        // private readonly UserManager<IdentityUser> _userManager;
        // private readonly SignInManager<IdentityUser> _
        private readonly ApplicationDbContext _context;
        private readonly ILogger<HomeController> _logger;

        private string searchText = string.Empty;
        private List<string> filteredResults = new();
        private List<string> nicheList = new();
        private List<string> p = new()
        {
            "Mary Bennett", "Marie Arseneau", "Leo Arseneau", "Joseph Arseneau", "Sarah Dick",
            "Dick Clarke", "Beatrice Dion", "Lorenzo Dion", "Lillian Doucette", "Aurelle Doucette"
        };

        public HomeController(ILogger<HomeController> logger, ApplicationDbContext context)
        {
            _context = context;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        [Route("/Privacy")]
        public IActionResult Privacy()
        {
            return View();
        }

        [Route("/About")]
        public IActionResult About()
        {
            return View();
        }

        [Route("/Contact")]
        public IActionResult Contact()
        {
            return View();
        }

        [HttpGet]
        [Route("/Reserve")]
        public IActionResult Reserve()
        {
            var plots = (from pd in _context.Plotdetails
                         where pd.PlotStatus == "Available"
                         join s in _context.Sections on pd.SectionId equals s.SectionId into sectionJoin
                         from s in sectionJoin.DefaultIfEmpty()
                         select new PlotListViewModel
                         {
                             PlotDetailsId = pd.PlotDetailsId,
                             SectionName = s != null ? s.SectionConstant : null,
                             Row = pd.Row,
                             Unit = pd.Unit,
                             Side = pd.Side,
                             Niche = pd.Niche,
                         }).ToList();

            return View(plots);
        }

        [Route("/Search")]
        public IActionResult Search(string? q)
        {
            List<SearchResultViewModel> results = new();

            if (!string.IsNullOrWhiteSpace(q))
            {
                var parts = q.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                var query = _context.Deceaseddetails.AsQueryable();

                foreach (var part in parts)
                {
                    var p = part;
                    query = query.Where(d =>
                        (d.FirstName != null && d.FirstName.Contains(p)) ||
                        (d.LastName != null && d.LastName.Contains(p)) ||
                        (d.MiddleName != null && d.MiddleName.Contains(p)));
                }

                results = (from d in query
                           join pd in _context.Plotdetails on d.PlotId equals pd.PlotDetailsId into plotJoin
                           from pd in plotJoin.DefaultIfEmpty()
                           join s in _context.Sections on pd.SectionId equals s.SectionId into sectionJoin
                           from s in sectionJoin.DefaultIfEmpty()
                           select new SearchResultViewModel
                           {
                               DeceasedDetailsId = d.DeceasedDetailsId,
                               FirstName = d.FirstName,
                               MiddleName = d.MiddleName,
                               LastName = d.LastName,
                               Gender = d.Gender,
                               DateBuried = d.DateBuried,
                               DOBYear = d.DOBYear,
                               DOBMonth = d.DOBMonth,
                               DOBDay = d.DOBDay,
                               DODYear = d.DODYear,
                               DODMonth = d.DODMonth,
                               DODDay = d.DODDay,
                               PlotId = d.PlotId,
                               ZoneId = d.ZoneId,
                               SectionName = s != null ? s.SectionConstant : null,
                               Row = pd != null ? pd.Row : null
                           }).ToList();
            }

            ViewData["Query"] = q;
            return View(results);
        }
        /*
        private void DoSearch()
        {
            if (string.IsNullOrWhiteSpace(searchText))
            {
                filteredResults = p;
            }
            else
            {
                filteredResults = p
                    .Where(i => i.Contains(searchText, StringComparison.OrdinalIgnoreCase))
                    .ToList();
            }
        }

        private List<string> DisplayNiche()
        {
            // Filler, just didnt want to hardcode values from 1-24.
            nicheList.Clear();
            for (int i = 1; i <= 24; i++)
            {
                nicheList.Add(i.ToString());
            }
            return nicheList;
        }

        private string SearchText
        {
            // Quick and dirty, but it works for the concept. Change it to FindAll(Object)
            // once we have some actual non-hardcoded values. May need to change it so it isn't querying the DB every keystroke?
            get => searchText;
            set
            {
                if (searchText != value)
                {
                    searchText = value;
                    filteredResults = string.IsNullOrWhiteSpace(searchText)
                        ? p
                        : p.Where(i => i.Contains(searchText, StringComparison.OrdinalIgnoreCase)).ToList();
                }
            }
        }
        */

        [HttpGet]
        [Route("/Reserve/{id:int}")]
        public IActionResult ReserveForm(int id)
        {
            var plot = (from pd in _context.Plotdetails
                        where pd.PlotDetailsId == id && pd.PlotStatus == "Available"
                        join s in _context.Sections on pd.SectionId equals s.SectionId into sectionJoin
                        from s in sectionJoin.DefaultIfEmpty()
                        select new ReservationFormViewModel
                        {
                            PlotDetailsId = pd.PlotDetailsId,
                            SectionName = s != null ? s.SectionConstant : null,
                            Row = pd.Row,
                            Unit = pd.Unit,
                            Side = pd.Side,
                            Niche = pd.Niche,
                        }).FirstOrDefault();

            if (plot == null) return NotFound();

            return View(plot);
        }

        [HttpPost]
        [Route("/Reserve/{id:int}")]
        [ValidateAntiForgeryToken]
        public IActionResult ReserveForm(int id, ReservationFormViewModel form)
        {
            // If no existing contact selected, first name and last name are required
            if (!form.ExistingContactId.HasValue)
            {
                if (string.IsNullOrWhiteSpace(form.FirstName))
                    ModelState.AddModelError("FirstName", "First name is required.");
                if (string.IsNullOrWhiteSpace(form.LastName))
                    ModelState.AddModelError("LastName", "Last name is required.");
            }

            if (!ModelState.IsValid)
            {
                var plot = (from pd in _context.Plotdetails
                            where pd.PlotDetailsId == id
                            join s in _context.Sections on pd.SectionId equals s.SectionId into sectionJoin
                            from s in sectionJoin.DefaultIfEmpty()
                            select new { s.SectionConstant, pd.Row, pd.Unit, pd.Side, pd.Niche }).FirstOrDefault();

                if (plot != null)
                {
                    form.PlotDetailsId = id;
                    form.SectionName = plot.SectionConstant;
                    form.Row = plot.Row;
                    form.Unit = plot.Unit;
                    form.Side = plot.Side;
                    form.Niche = plot.Niche;
                }

                return View(form);
            }

            var isAvailable = _context.Plotdetails
                .Any(p => p.PlotDetailsId == id && p.PlotStatus == "Available");

            if (!isAvailable) return Conflict("This plot is no longer available.");

            var now = DateTime.Now;

            using var transaction = _context.Database.BeginTransaction();

            int contactId;
            if (form.ExistingContactId.HasValue)
            {
                var exists = _context.Contactdetails.Any(c => c.ContactDetailsId == form.ExistingContactId.Value);
                if (!exists) return BadRequest("Selected contact no longer exists.");
                contactId = form.ExistingContactId.Value;
            }
            else
            {
                var contact = new GraveyardGISApp.Data.Entities.Contactdetail
                {
                    FirstName = form.FirstName!,
                    MiddleName = form.MiddleName,
                    LastName = form.LastName!,
                    PhoneNumber = form.PhoneNumber,
                    Email = form.Email,
                    Address = form.Address,
                    CreatedDate = now,
                    CreatedBy = 1,
                };
                _context.Contactdetails.Add(contact);
                _context.SaveChanges();
                contactId = contact.ContactDetailsId;
            }

            _context.Plotcontactmappings.Add(new GraveyardGISApp.Data.Entities.Plotcontactmapping
            {
                PlotDetailsId = id,
                ContactDetailsId = contactId,
                IsPrimaryContact = true,
                CreatedDate = now,
                CreatedBy = 1,
            });

            _context.Paymentdetails.Add(new GraveyardGISApp.Data.Entities.Paymentdetail
            {
                PlotId = id,
                ContactDetailsId = contactId,
                PaymentStatusId = 2, // UNPAID
                BalanceDue = form.BalanceDue,
                BalancePaid = 0,
                CreatedDate = now,
                CreatedBy = 1,
            });

            _context.SaveChanges();

            _context.Plotdetails
                .Where(p => p.PlotDetailsId == id)
                .ExecuteUpdate(s => s
                    .SetProperty(p => p.PlotStatus, "Reserved")
                    .SetProperty(p => p.IsAvailable, false));

            transaction.Commit();

            return RedirectToAction(nameof(Reserve));
        }

        [Route("/Deceased/{id:int}")]
        public IActionResult Deceased(int id)
        {
            var detail = (from d in _context.Deceaseddetails
                          where d.DeceasedDetailsId == id
                          join pd in _context.Plotdetails on d.PlotId equals pd.PlotDetailsId into plotJoin
                          from pd in plotJoin.DefaultIfEmpty()
                          join s in _context.Sections on pd.SectionId equals s.SectionId into sectionJoin
                          from s in sectionJoin.DefaultIfEmpty()
                          select new DeceasedDetailViewModel
                          {
                              DeceasedDetailsId = d.DeceasedDetailsId,
                              FirstName = d.FirstName,
                              MiddleName = d.MiddleName,
                              LastName = d.LastName,
                              Gender = d.Gender,
                              DateBuried = d.DateBuried,
                              DOBYear = d.DOBYear,
                              DOBMonth = d.DOBMonth,
                              DOBDay = d.DOBDay,
                              DODYear = d.DODYear,
                              DODMonth = d.DODMonth,
                              DODDay = d.DODDay,
                              PlotId = d.PlotId,
                              ZoneId = d.ZoneId,
                              SectionName = s != null ? s.SectionConstant : null,
                              Row = pd != null ? pd.Row : null,
                              Unit = pd != null ? pd.Unit : null,
                              Side = pd != null ? pd.Side : null,
                              Niche = pd != null ? pd.Niche : null,
                          }).FirstOrDefault();

            if (detail == null) return NotFound();

            detail.DeceasedContacts = (from m in _context.Deceasedcontactmappings
                                        where m.DeceasedDetailsId == id
                                        join c in _context.Contactdetails on m.ContactDetailsId equals c.ContactDetailsId
                                        select new ContactViewModel
                                        {
                                            FirstName = c.FirstName,
                                            MiddleName = c.MiddleName,
                                            LastName = c.LastName,
                                            PhoneNumber = c.PhoneNumber,
                                            Email = c.Email,
                                            Address = c.Address,
                                            RelationshipType = m.RelationshipType,
                                            IsPrimaryContact = m.IsPrimaryContact
                                        }).ToList();

            detail.PlotContacts = (from m in _context.Plotcontactmappings
                                    where m.PlotDetailsId == detail.PlotId
                                    join c in _context.Contactdetails on m.ContactDetailsId equals c.ContactDetailsId
                                    select new ContactViewModel
                                    {
                                        FirstName = c.FirstName,
                                        MiddleName = c.MiddleName,
                                        LastName = c.LastName,
                                        PhoneNumber = c.PhoneNumber,
                                        Email = c.Email,
                                        Address = c.Address,
                                        RelationshipType = null,
                                        IsPrimaryContact = m.IsPrimaryContact
                                    }).ToList();

            return View(detail);
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
