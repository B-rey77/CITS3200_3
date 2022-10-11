# Generated by Django 4.1 on 2022-10-11 09:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0019_remove_users_is_admin_alter_users_is_active_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="isapproved_False_results",
            fields=[],
            options={
                "verbose_name": "Results (Pending Approval)",
                "verbose_name_plural": "Results (Pending Approval)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.results",),
        ),
        migrations.CreateModel(
            name="isapproved_False_studies",
            fields=[],
            options={
                "verbose_name": "Studies (Pending Approval)",
                "verbose_name_plural": "Studies (Pending Approval)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.studies",),
        ),
        migrations.CreateModel(
            name="Studygroup.ARF_studies",
            fields=[],
            options={
                "verbose_name": "ARF Studies",
                "verbose_name_plural": "ARF Studies",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.studies",),
        ),
        migrations.CreateModel(
            name="Studygroup.ASPGN_studies",
            fields=[],
            options={
                "verbose_name": "ASPGN Studies",
                "verbose_name_plural": "ASPGN Studies",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.studies",),
        ),
        migrations.CreateModel(
            name="Studygroup.IG_studies",
            fields=[],
            options={
                "verbose_name": "Invasive GAS Studies",
                "verbose_name_plural": "Invasive GAS Studies",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.studies",),
        ),
        migrations.CreateModel(
            name="Studygroup.SST_studies",
            fields=[],
            options={
                "verbose_name": "Superficial Skin & Throat Studies",
                "verbose_name_plural": "Superficial Skin & Throat Studies",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.studies",),
        ),
        migrations.CreateModel(
            name="StudyStudygroup.ARF_results",
            fields=[],
            options={
                "verbose_name": "ARF Results",
                "verbose_name_plural": "ARF Results",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.results",),
        ),
        migrations.CreateModel(
            name="StudyStudygroup.ASPGN_results",
            fields=[],
            options={
                "verbose_name": "ASPGN Results",
                "verbose_name_plural": "ASPGN Results",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.results",),
        ),
        migrations.CreateModel(
            name="StudyStudygroup.IG_results",
            fields=[],
            options={
                "verbose_name": "Invasive GAS Results",
                "verbose_name_plural": "Invasive GAS Results",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.results",),
        ),
        migrations.CreateModel(
            name="StudyStudygroup.SST_results",
            fields=[],
            options={
                "verbose_name": "Superficial Skin & Throat Results",
                "verbose_name_plural": "Superficial Skin & Throat Results",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("database.results",),
        ),
        migrations.AlterModelOptions(
            name="results",
            options={
                "verbose_name": "Result (Any Group)",
                "verbose_name_plural": "Results (Any Group)",
            },
        ),
        migrations.AlterModelOptions(
            name="studies",
            options={
                "verbose_name": "Study (Any Group)",
                "verbose_name_plural": "Studies (Any Group)",
            },
        ),
        migrations.AlterModelOptions(
            name="users",
            options={"verbose_name_plural": "Users"},
        ),
        migrations.RemoveField(
            model_name="results",
            name="Point_estimate_original",
        ),
        migrations.RemoveField(
            model_name="studies",
            name="Case_cap_meth",
        ),
        migrations.RemoveField(
            model_name="studies",
            name="Case_findings_other",
        ),
        migrations.AddField(
            model_name="results",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Results Added By User",
            ),
        ),
        migrations.AddField(
            model_name="results",
            name="is_approved",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this study has been approved or is pending approval.",
                verbose_name="Results Approved",
            ),
        ),
        migrations.AddField(
            model_name="studies",
            name="Clinical_definition_category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Undefined or unknown", "Undefined or unknown"),
                    (
                        "Both confirmed and probable cases",
                        "Both confirmed and probable cases",
                    ),
                    ("Confirmed case", "Confirmed case"),
                    ("Definite and probable ARF", "Definite and probable ARF"),
                    ("Suspected or probable case", "Suspected or probable case"),
                    ("Other", "Other"),
                ],
                help_text="Category for capturing the disease classification that was included in the study, if reported. Classifications depend on the disease and can include confirmed, suspected, probably, active, inactive, recurrent, total, undefined or unknown, subclinical or asymptomatic.",
                max_length=50,
                null=True,
                verbose_name="Clinical definition category",
            ),
        ),
        migrations.AddField(
            model_name="studies",
            name="Surveillance_setting",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Unknown", "Unknown"),
                    ("Community", "Community"),
                    ("Hospital", "Hospital"),
                    ("Household", "Household"),
                    ("Laboratory", "Laboratory"),
                    ("Multiple", "Multiple"),
                    ("Primary health centre", "Primary health centre"),
                    ("School", "School"),
                    ("Other", "Other"),
                ],
                help_text="The type of institution where the study was conducted. Classifications include primary health care clinic (PHC), tertiary hospital, outpatient clinics, school clinics, households, early childhood centers, aged care facilities etc.",
                max_length=25,
                null=True,
                verbose_name="Surveillance setting",
            ),
        ),
        migrations.AddField(
            model_name="studies",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Study Added By User",
            ),
        ),
        migrations.AddField(
            model_name="studies",
            name="is_approved",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this study has been approved or is pending approval.",
                verbose_name="Study Approved",
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Age_general",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ALL", "All"),
                    ("AD", "Adult"),
                    ("C", "Children"),
                    ("AL", "Adolescents"),
                    ("EA", "Elderly Adults"),
                    ("I", "Infant"),
                    ("M", "Mix"),
                    ("N/A", "N/A"),
                ],
                max_length=5,
                verbose_name="Age Category (General)",
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Age_original",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Age Category"
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Age_standardisation",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate is age-standardised and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Country",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Country where study was conducted (for future use, in the case that international studies are added to the data collection).",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Dataset_name",
            field=models.BooleanField(
                blank=True, help_text="Empty variable", null=True
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Defined_ARF",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate has defined ARF and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Focus_of_study",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Short sentence which summarises the focus of the study, to assist with interpreting the burden estimate.",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="GAS_attributable_fraction",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate is a proportion which is GAS-specific and therefore represents a GAS-attributable fraction and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Indigenous_population",
            field=models.CharField(
                blank=True,
                default="",
                help_text="This variable captures stratification of the Indigenous population (where reported) into “Aboriginal”, “Torres Strait Islander” or “both Aboriginal and Torres Strait Islanders”.",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Indigenous_status",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Population - Indigenous Status"
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Interpolated_from_graph",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate is interpolated and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Jurisdiction",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Jurisdictional location of the study, categorized by individual jurisdiction name (WA, NT, SA, QLD, NSW, Vic) or combination of jurisdictions (Combination – Northern Australia or Combination- others). ",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Mortality_flag",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate is a mortality estimate and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Observation_time_years",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Total observation time used by the study for generating the point estimate. ",
                max_digits=5,
                null=True,
                validators=[django.core.validators.MaxValueValidator(150.0)],
                verbose_name="Observational period,",
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Point_estimate",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="results",
            name="Population_gender",
            field=models.CharField(
                blank=True,
                help_text="This variable captures stratification by sex (where reported), with categories of “males”, “females”, “males and females”. ",
                max_length=30,
                verbose_name="Population - Gender",
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Proportion",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate is a proportion and “0” or “N/A” otherwise.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Recurrent_ARF_flag",
            field=models.BooleanField(
                blank=True,
                help_text="Indicator variable which is “1” if point estimate includes recurrent ARF and “0” or “N/A” otherwise (applicable to ARF burden estimates only).",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Specific_location",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Point estimates stratified by specific geographic locations (where reported), for example: Kimberley, Far North Queensland or Central Australia.",
                max_length=100,
                verbose_name="Specific geographic locations",
            ),
        ),
        migrations.AlterField(
            model_name="results",
            name="Study",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="database.studies",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Age_general",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Age Category (General)"
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Age_original",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Age Category"
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Aria_remote",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Classification into metropolitan, regional and remote areas based on the ARIA+ (Accessibility and Remoteness Index of Australia) system.",
                max_length=200,
                verbose_name="Remoteness",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Burden_measure",
            field=models.CharField(
                blank=True,
                help_text="The epidemiological measure presented as a point estimate by the study. The categories include: population incidence, population prevalence or proportion (not population based).",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Case_cap_meth_other",
            field=models.CharField(
                blank=True,
                help_text="Previously called Case_cap_meth_other",
                max_length=200,
                null=True,
                verbose_name="Clinical definition category (Other)",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Case_definition",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Indicates the process used to identify Strep A-associated diseases, such as: notifications, ICD codes, Snowmed/ICPC codes, clinical diagnosis, laboratory diagnosis, echocardiography or combined methods.   ",
                max_length=200,
                verbose_name="Case definition method",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Case_findings",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Method of case identification, for example: screening or active surveillance for reporting cases of impetigo or skin sores; population registers for ARF; medical record review.",
                max_length=200,
                verbose_name="Case finding method",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Climate",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Climatic conditions based on the geographic coverage of studies, for example: “Tropical” for studies conducted at the Top-End NT, “Temperate” for studies from Victoria or NSW. ",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Coverage",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Level of geographic coverage in the study, categorised as (i) national/multli-jurisdictional, (ii) state, (iii) subnational/ regional, (iv) single institution/ service.",
                max_length=200,
                verbose_name="Geographic Coverage",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Data_source",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Name of the dataset, project, consortium or specific disease register.",
                max_length=200,
                verbose_name="Data source (if applicable)",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Jurisdiction",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Jurisdictional location of the study, categorized by individual jurisdiction name (WA, NT, SA, QLD, NSW, Vic) or combination of jurisdictions (Combination – Northern Australia or Combination- others). ",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Method_limitations",
            field=models.BooleanField(
                blank=True,
                help_text="This variable indicates whether method limitations were specified by the authors of the publication.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Mortality_data",
            field=models.BooleanField(
                blank=True,
                help_text="This variable indicates “Yes/No”, whether mortality estimates are reported by the study.",
                null=True,
                verbose_name="Mortality",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Other_points",
            field=models.TextField(
                blank=True,
                default="",
                help_text="This variable captures any other relevant notes relating to the study that may impact the interpretation of Strep A burden estimates.",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Paper_link",
            field=models.CharField(
                blank=True,
                help_text="URL or doi to facilitate access to the source manuscript/report, full access will depend on open/institutional access permissions set by each journal.",
                max_length=200,
                verbose_name="Link to Paper Download",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Paper_title",
            field=models.CharField(
                help_text="Title of the published manuscript/report.",
                max_length=200,
                verbose_name="Paper Title",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Population_denom",
            field=models.CharField(
                blank=True,
                default="",
                help_text="The population used as the denominator by the study, for example: general population, Indigenous population, hospitalised patients.",
                max_length=200,
                verbose_name="Population denominator",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Population_group_strata",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Indicates whether burden estimates were presented stratified by population group or not i.e.) Yes – then Indigenous vs. non-Indigenous results are presented, No – general population burden estimates only with no stratification.",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Ses_reported",
            field=models.BooleanField(
                blank=True,
                help_text="This variable indicates “Yes/No”, whether socioeconomic status is reported by the study.",
                null=True,
                verbose_name="Socioeconomic status (SES) reported",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Specific_region",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Specific region covered by the study, for example: city / town if the study involved a single institution / service; or number and location of remote communities included. ",
                max_length=200,
                verbose_name="Specific region (if applicable)",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Study_description",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Name of the first author, abbreviated name of journal and year of manuscript publication. Example: McDonald, Clin Infect Dis, 2006",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Study_design",
            field=models.CharField(
                choices=[
                    ("CS", "Case series"),
                    ("CST", "Cross-sectional"),
                    ("P", "Prospective"),
                    ("PRP", "Prospective and Retrospective"),
                    ("PC", "Prospective cohort"),
                    ("R", "Report"),
                    ("RP", "Retrospective"),
                    ("RPR", "Retrospective review"),
                    ("RPC", "Retrospective cohort"),
                    ("RA", "Review article"),
                    ("O", "Other"),
                ],
                help_text="Study classification based on the temporality of data collection. Prospective (if study involves screening or active surveillance or primary data collection) or retrospective (study involves using either administrative/medical record data from hospitals, primary health centres, laboratory or population datasets) or both prospective and retrospective (if study has both components). Other categories which are rarely used include report and outbreak investigation.",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Study_design_other",
            field=models.CharField(
                blank=True,
                max_length=1000,
                null=True,
                verbose_name="Study design (Other)",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Study_group",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SST", "Superficial skin and throat"),
                    ("IG", "Invasive GAS"),
                    ("ARF", "ARF"),
                    ("ASPGN", "APSGN"),
                ],
                help_text="Broad classification of the Strep A-associated disease type that the study was based on: (i) Superficial skin and/or throat infections, (ii) Invasive Strep A infections, (iii) Acute Rheumatic Fever (ARF), (iv) Acute Post Streptococcal Glomerulonephritis (APSGN).",
                max_length=5,
                verbose_name="Study Group",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Unique_identifier",
            field=models.CharField(
                blank=True,
                help_text="Links the methods dataset to the results dataset, which contains estimates reported by the same study (often multiple results per study). Each Unique Identifier consists of the year of publication followed by the first four letters of the first author. Example: 2006MCDO is a unique identifier for McDonald, Clin Infect Dis, 2006, which provides a link between the methods used by 2006MCDO to obtain the 21 estimates reported in that manuscript. ",
                max_length=12,
                null=True,
                verbose_name="Unique Identifier",
            ),
        ),
        migrations.AlterField(
            model_name="studies",
            name="Year",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Year of publication of manuscript/report.",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1900),
                    django.core.validators.MaxValueValidator(2100),
                ],
                verbose_name="Publication Year",
            ),
        ),
    ]
